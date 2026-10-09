from agents.requirement_agent import generate_requirements
from agents.documentation_agent import generate_srs
from database.db import save_project

project = "Online Food Delivery System"

requirements = generate_requirements(project)

srs = generate_srs(requirements)

save_project(
    project,
    requirements,
    srs
)

print("Saved successfully!")