from langchain_ollama import OllamaLLM
import concurrent.futures


# ============================================================
# LLM CONFIGURATION
# ============================================================

def create_llm(model="llama3.2"):
    """
    Creates the Ollama LLM used by the Requirement Agent.
    """

    return OllamaLLM(
        model=model,
        temperature=0.2,
        top_k=10,
        top_p=0.95,
        num_predict=2500,
        num_ctx=8192,
        repeat_penalty=1.05
    )


# ============================================================
# COMMON MESSAGE
# ============================================================

NO_ANSWER_MESSAGE = (
    "I can't generate output for this question. "
    "Please provide a software project idea or requirement "
    "that can be analyzed by the Requirement Agent."
)


# ============================================================
# SAFE LLM INVOCATION
# ============================================================

def safe_invoke(
    llm,
    prompt: str,
    timeout: int = 900,
    fallback: str | None = None
) -> str:
    """
    Invokes the LLM safely with a timeout.
    """

    if fallback is None:
        fallback = NO_ANSWER_MESSAGE

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    future = executor.submit(llm.invoke, prompt)

    try:
        result = future.result(timeout=timeout)

        if result is None:
            return fallback

        return str(result).strip()

    except concurrent.futures.TimeoutError:
        return (
            f"{fallback}\n\n"
            f"The model timed out after {timeout} seconds."
        )

    except Exception as exc:
        return (
            f"{fallback}\n\n"
            f"Model error: {exc}"
        )

    finally:
        executor.shutdown(wait=False)


# ============================================================
# PROJECT REQUEST VALIDATION
# ============================================================

def is_project_request(text: str) -> bool:
    """
    Checks whether the supplied text is related to a
    software/project requirement.
    """

    if not isinstance(text, str) or not text.strip():
        return False

    text = text.lower().strip()

    negative_phrases = [
        "tell me about yourself",
        "who are you",
        "what can you do",
        "introduce yourself",
        "yourself",
        "what is your name",
        "how are you",
        "personal",
        "hobby",
        "favorite",
        "love",
        "career",
    ]

    if any(phrase in text for phrase in negative_phrases):
        return False

    keywords = [
        "project",
        "system",
        "application",
        "app",
        "website",
        "software",
        "platform",
        "product",
        "requirements",
        "requirement",
        "feature",
        "user story",
        "user stories",
        "module",
        "service",
        "solution",
        "tool",
        "dashboard",
        "ecommerce",
        "management",
        "crm",
        "erp",
        "inventory",
        "booking",
        "delivery",
        "payment",
        "reservation",
        "chatbot",
        "assistant",
        "portal",
        "system design",
        "workflow",
        "business",
        "database",
        "api",
        "web application",
        "mobile application",
    ]

    return any(keyword in text for keyword in keywords)


# ============================================================
# RAG CONTEXT
# ============================================================

def get_context(project_idea: str) -> str:
    """
    Retrieves relevant context from the project's RAG system.

    If the RAG module is unavailable, the agent continues
    using the project idea directly.
    """

    try:
        from rag.retriever import get_context as rag_get_context

        context = rag_get_context(project_idea)

        if context:
            return str(context)

    except ImportError:
        pass

    except Exception:
        pass

    return ""


# ============================================================
# REQUIREMENT GENERATION
# ============================================================

def generate_requirements(project_idea: str) -> str:
    """
    Generates detailed software requirements for a project.

    This is the function imported by streamlit_app.py.
    """

    if not isinstance(project_idea, str) or not project_idea.strip():
        return (
            "Please enter a valid software project idea."
        )

    project_idea = project_idea.strip()

    # Validate whether the request is project-related
    if not is_project_request(project_idea):
        return NO_ANSWER_MESSAGE

    # --------------------------------------------------------
    # Retrieve relevant project-document context
    # --------------------------------------------------------

    context = get_context(project_idea)

    if not context:
        context = (
            "No additional reference document context was "
            "retrieved. Analyze the project idea directly "
            "without inventing external document references."
        )

    # --------------------------------------------------------
    # Requirement Engineering Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an expert Software Requirement Engineer.

Your task is to analyze the following software project idea
and generate a complete, structured requirement specification.

PROJECT IDEA:
{project_idea}

REFERENCE CONTEXT FROM PROJECT DOCUMENTS:
{context}

IMPORTANT RULES:

1. Understand the complete project idea before generating output.
2. Do not give a generic answer.
3. Include requirements specifically related to the project.
4. Do not invent technologies or features that contradict the project.
5. Clearly separate functional and non-functional requirements.
6. Include realistic user stories.
7. Define the project scope clearly.
8. Include important modules/features.
9. Mention actors/users involved in the system.
10. Make requirements specific enough for software development.
11. Avoid unnecessary explanations.
12. Use professional Software Requirement Engineering terminology.
13. Do not answer personal/general questions.
14. Do not mention that you are an AI unless necessary.

Generate the output using exactly the following structure:

============================================================
REQUIREMENT SPECIFICATION
============================================================

1. PROJECT OVERVIEW
- Project Name
- Problem Statement
- Proposed Solution
- Target Users
- Main Objective

2. SYSTEM ACTORS
List all important users, administrators, external systems,
or other actors interacting with the system.

3. FUNCTIONAL REQUIREMENTS
Provide detailed functional requirements.

Use the format:

FR-01:
FR-02:
FR-03:
...

Each requirement must describe a specific system behavior.

4. NON-FUNCTIONAL REQUIREMENTS

Performance:
Security:
Scalability:
Reliability:
Availability:
Usability:
Maintainability:
Privacy:
Data Integrity:

5. USER STORIES

Use the format:

US-01:
As a <user>, I want <feature>, so that <benefit>.

US-02:
...

6. SYSTEM MODULES

For every major module provide:

Module Name:
Purpose:
Main Functions:

7. INPUT REQUIREMENTS

List the important inputs/data required by the system.

8. OUTPUT REQUIREMENTS

List the important outputs/results generated by the system.

9. BUSINESS RULES

List important rules and constraints governing the system.

10. DATA REQUIREMENTS

Describe the major data entities and information that
the system needs to store or process.

11. PROJECT SCOPE

IN SCOPE:
List the features included in the project.

OUT OF SCOPE:
List realistic features that are intentionally excluded.

12. ASSUMPTIONS AND CONSTRAINTS

Assumptions:
Constraints:

13. ACCEPTANCE CRITERIA

Provide important high-level criteria that can be used
to determine whether the system satisfies its requirements.

Make the final answer detailed, structured, and directly
usable by the Documentation, Architecture, and QA agents.
"""

    # --------------------------------------------------------
    # Create LLM
    # --------------------------------------------------------

    try:
        llm = create_llm()
    except Exception as exc:
        return (
            "Unable to initialize the Ollama model.\n\n"
            f"Error: {exc}"
        )

    # --------------------------------------------------------
    # Generate requirements
    # --------------------------------------------------------

    result = safe_invoke(
        llm,
        prompt,
        timeout=900,
        fallback=NO_ANSWER_MESSAGE
    )

    return result


# ============================================================
# ALIAS FOR COMPATIBILITY
# ============================================================

def run_requirement_agent(project_idea: str) -> str:
    """
    Compatibility wrapper for other modules that may call
    the Requirement Agent using run_requirement_agent().
    """

    return generate_requirements(project_idea)


# ============================================================
# TEST / DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    test_project = """
    Online Pharmacy Management System that allows customers
    to search medicines, upload prescriptions, place orders,
    make payments, track deliveries, and allows pharmacists
    and administrators to manage medicines, prescriptions,
    inventory, orders, and users.
    """

    print("\nGenerating requirements...\n")

    output = generate_requirements(test_project)

    print(output)