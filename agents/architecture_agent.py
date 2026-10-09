from agents.llm_utils import create_llm, safe_invoke

llm = create_llm()

def generate_architecture(requirements):

    prompt = f"""
Requirements:

{requirements}

Generate a detailed software architecture.

Include:

1. High Level Architecture
2. System Components
3. Frontend Architecture
4. Backend Architecture
5. Database Architecture
6. API Architecture
7. Authentication Flow
8. User Workflow
9. Deployment Architecture
10. Technology Stack
11. Database Tables
12. Security Architecture
13. Scalability Considerations

Provide detailed explanations.
"""

    return safe_invoke(llm, prompt)