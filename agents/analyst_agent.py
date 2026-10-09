from agents.llm_utils import create_llm, is_project_request, NO_ANSWER_MESSAGE, safe_invoke

llm = create_llm()

def analyze_project(project):

    if not is_project_request(project):
        return NO_ANSWER_MESSAGE

    prompt = f"""
You are a Senior Business Analyst.

Project:
{project}

Generate a detailed Business Analysis Report.

Include:

1. Project Overview
2. Problem Statement
3. Business Objectives (minimum 5)
4. Stakeholders (minimum 5)
5. Stakeholder Responsibilities
6. Business Risks (minimum 5)
7. Risk Mitigation Strategies
8. Assumptions
9. Constraints
10. Project Scope
11. Out of Scope Items
12. Expected Benefits

Provide detailed explanations.
"""

    return safe_invoke(llm, prompt)