from agents.llm_utils import create_llm, safe_invoke


# ============================================================
# QA / TEST CASE AGENT
# ============================================================

def generate_test_cases(requirements: str) -> str:
    """
    Generates Functional, Integration, and Acceptance
    Test Cases from the generated requirements.
    """

    if not requirements or not requirements.strip():
        return "No requirements were provided for test case generation."

    # Create LLM
    llm = create_llm()

    prompt = f"""
You are a professional Software Quality Assurance Engineer.

Analyze the following software requirements and create
detailed test cases for the SAME project.

============================================================
REQUIREMENTS
============================================================

{requirements}

============================================================
TEST CASE GENERATION TASK
============================================================

Generate exactly:

1. 5 Functional Test Cases
2. 3 Integration Test Cases
3. 3 Acceptance Test Cases

TOTAL = 11 TEST CASES

============================================================
IMPORTANT RULES
============================================================

1. All test cases must be directly related to the given
   requirements.

2. Do not create generic or unrelated test cases.

3. Do not change the project domain.

4. Each test case must contain:
   - Test Case ID
   - Test Type
   - Scenario
   - Preconditions
   - Test Steps
   - Expected Result

5. Functional test cases must verify individual system
   functions.

6. Integration test cases must verify interaction between
   different modules, services, APIs, databases, or system
   components.

7. Acceptance test cases must verify important end-to-end
   business requirements from the user's perspective.

8. Test steps should be clear and sequential.

9. Expected results must be specific and measurable.

10. Use IDs:
    FT-01 to FT-05 for Functional Test Cases
    IT-01 to IT-03 for Integration Test Cases
    AT-01 to AT-03 for Acceptance Test Cases

11. Do not omit any requested test case.

12. Return the result in Markdown table format.

============================================================
OUTPUT FORMAT
============================================================

## FUNCTIONAL TEST CASES

| Test Case ID | Test Type | Scenario | Preconditions | Test Steps | Expected Result |
|--------------|-----------|----------|---------------|------------|-----------------|
| FT-01 | Functional | ... | ... | 1. ... 2. ... | ... |
| FT-02 | Functional | ... | ... | 1. ... 2. ... | ... |
| FT-03 | Functional | ... | ... | 1. ... 2. ... | ... |
| FT-04 | Functional | ... | ... | 1. ... 2. ... | ... |
| FT-05 | Functional | ... | ... | 1. ... 2. ... | ... |

## INTEGRATION TEST CASES

| Test Case ID | Test Type | Scenario | Preconditions | Test Steps | Expected Result |
|--------------|-----------|----------|---------------|------------|-----------------|
| IT-01 | Integration | ... | ... | 1. ... 2. ... | ... |
| IT-02 | Integration | ... | ... | 1. ... 2. ... | ... |
| IT-03 | Integration | ... | ... | 1. ... 2. ... | ... |

## ACCEPTANCE TEST CASES

| Test Case ID | Test Type | Scenario | Preconditions | Test Steps | Expected Result |
|--------------|-----------|----------|---------------|------------|-----------------|
| AT-01 | Acceptance | ... | ... | 1. ... 2. ... | ... |
| AT-02 | Acceptance | ... | ... | 1. ... 2. ... | ... |
| AT-03 | Acceptance | ... | ... | 1. ... 2. ... | ... |

============================================================
FINAL CHECK
============================================================

Before returning the answer, verify that there are:

- Exactly 5 Functional Test Cases
- Exactly 3 Integration Test Cases
- Exactly 3 Acceptance Test Cases
- Exactly 11 Test Cases in total

Do not provide fewer than 11 test cases.
"""

    result = safe_invoke(
        llm,
        prompt,
        timeout=900,
        fallback="Unable to generate test cases."
    )

    return result


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    sample_requirements = """
    Online Pharmacy Management System.

    Customers can register and log in.
    Customers can search medicines.
    Customers can upload prescriptions.
    Customers can place medicine orders.
    Customers can make payments.
    Customers can track deliveries.

    Pharmacists can verify prescriptions.
    Administrators can manage medicines and inventory.
    """

    print("\nGenerating test cases...\n")

    test_cases = generate_test_cases(sample_requirements)

    print(test_cases)