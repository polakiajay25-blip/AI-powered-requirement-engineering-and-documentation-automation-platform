from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.analyst_agent import analyze_project
from agents.llm_utils import is_project_request, NO_ANSWER_MESSAGE
from agents.requirement_agent import generate_requirements
from agents.documentation_agent import generate_srs
from agents.architecture_agent import generate_architecture
from agents.qa_agent import generate_test_cases

app = FastAPI(
    title="AI Requirement Engineering API",
    version="1.0"
)

# ---------------------
# Request Model
# ---------------------

class ProjectRequest(BaseModel):
    project_idea: str 


# ---------------------
# Health Check
# ---------------------

@app.get("/")
def home():
    return {
        "message": "AI Requirement Engineering API Running"
    }


# ---------------------
# Analyst Agent
# ---------------------

@app.post("/analyze")
def analyze(req: ProjectRequest):

    if not is_project_request(req.project_idea):
        raise HTTPException(status_code=400, detail=NO_ANSWER_MESSAGE)

    result = analyze_project(
        req.project_idea
    )

    return {
        "analysis": result
    }


# ---------------------
# Requirement Agent
# ---------------------

@app.post("/requirements")
def requirements(req: ProjectRequest):

    if not is_project_request(req.project_idea):
        raise HTTPException(status_code=400, detail=NO_ANSWER_MESSAGE)

    result = generate_requirements(
        req.project_idea
    )

    return {
        "requirements": result
    }


# ---------------------
# Full Workflow
# ---------------------

@app.post("/generate-all")
def generate_all(req: ProjectRequest):

    if not is_project_request(req.project_idea):
        raise HTTPException(status_code=400, detail=NO_ANSWER_MESSAGE)

    analysis = analyze_project(
        req.project_idea
    )

    requirements = generate_requirements(
        req.project_idea
    )

    srs = generate_srs(
        requirements
    )

    architecture = generate_architecture(
        requirements
    )

    tests = generate_test_cases(
        requirements
    )

    return {
        "analysis": analysis,
        "requirements": requirements,
        "srs": srs,
        "architecture": architecture,
        "test_cases": tests
    }