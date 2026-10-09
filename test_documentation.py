from agents.requirement_agent import generate_requirements
from agents.documentation_agent import generate_srs

req = generate_requirements(
    "Online Food Delivery System"
)

srs = generate_srs(req)

print(srs)