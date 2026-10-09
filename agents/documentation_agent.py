from agents.llm_utils import create_llm, safe_invoke

llm = create_llm()

def generate_srs(requirements):

    prompt = f"""
You are a Senior Software Architect.

Create an IEEE Software Requirement Specification (SRS).

Project Requirements:

{requirements}

Generate the document in the following format.

# 1. Introduction
- Purpose
- Scope
- Definitions

# 2. Overall Description
- Product Perspective
- Product Functions
- User Classes
- Operating Environment

# 3. Functional Requirements
Provide all functional requirements in numbered format:
FR-1
FR-2
FR-3
...

# 4. Non Functional Requirements
Provide all non-functional requirements in numbered format:
NFR-1
NFR-2
NFR-3
...

# 5. External Interface Requirements
- User Interface
- Software Interface
- Hardware Interface
- Communication Interface

# 6. Security Requirements

# 7. Performance Requirements

# 8. Assumptions

# 9. Constraints

# 10. Future Enhancements

Rules:
- Keep each section concise.
- Use bullet points.
- Do not repeat information.
- Complete every section.
- Limit total output to approximately 1200 words.
"""

    return safe_invoke(llm, prompt)