from agents.llm_utils import create_llm, NO_ANSWER_MESSAGE, is_project_request, safe_invoke
from rag.retriever import get_context

llm = create_llm()

def generate_requirements(project_idea):

    if not is_project_request(project_idea):
        return NO_ANSWER_MESSAGE

    context = get_context(project_idea)

    if not context.strip():
        return NO_ANSWER_MESSAGE

    prompt = f"""
Reference Documents:

{context}

Project:
{project_idea}

Generate detailed requirements.

Include:

1. Project Purpose
2. Project Scope

Functional Requirements:
- Generate at least 10 functional requirements

Non Functional Requirements:
- Generate at least 5 non-functional requirements

User Stories:
- Generate at least 5 user stories

Business Rules:
- Generate at least 3 business rules

Assumptions:
- Generate at least 3 assumptions

Constraints:
- Generate at least 3 constraints

Provide detailed output.
"""

    return safe_invoke(llm, prompt)