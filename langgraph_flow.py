from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.analyst_agent import analyze_project
from agents.requirement_agent import generate_requirements
from agents.documentation_agent import generate_srs
from agents.architecture_agent import generate_architecture
from agents.qa_agent import generate_test_cases

from database.db import create_db, save_project

# -----------------------------------
# CREATE DATABASE
# -----------------------------------

create_db()

# -----------------------------------
# STATE
# -----------------------------------

class ProjectState(TypedDict):
    project: str
    analysis: str
    requirements: str
    srs: str
    architecture: str
    tests: str


# -----------------------------------
# ANALYST NODE
# -----------------------------------

def analyst_node(state):

    print("Running Analyst Agent...")

    state["analysis"] = analyze_project(
        state["project"]
    )

    return state


# -----------------------------------
# REQUIREMENT NODE
# -----------------------------------

def requirement_node(state):

    print("Running Requirement Agent...")

    state["requirements"] = generate_requirements(
        state["project"]
    )

    return state


# -----------------------------------
# SRS NODE
# -----------------------------------

def srs_node(state):

    print("Running Documentation Agent...")

    state["srs"] = generate_srs(
        state["requirements"]
    )

    return state


# -----------------------------------
# ARCHITECTURE NODE
# -----------------------------------

def architecture_node(state):

    print("Running Architecture Agent...")

    state["architecture"] = generate_architecture(
        state["requirements"]
    )

    return state


# -----------------------------------
# QA NODE
# -----------------------------------

def qa_node(state):

    print("Running QA Agent...")

    state["tests"] = generate_test_cases(
        state["requirements"]
    )

    return state


# -----------------------------------
# SAVE NODE
# -----------------------------------

def save_node(state):

    print("Saving Project To Database...")

    save_project(
        state["project"],
        state["analysis"],
        state["requirements"],
        state["srs"],
        state["architecture"],
        state["tests"]
    )

    print("Project Saved Successfully!")

    return state


# -----------------------------------
# BUILD GRAPH
# -----------------------------------

graph = StateGraph(ProjectState)

graph.add_node("analyst", analyst_node)
graph.add_node("requirements", requirement_node)
graph.add_node("srs", srs_node)
graph.add_node("architecture", architecture_node)
graph.add_node("qa", qa_node)
graph.add_node("save", save_node)

graph.set_entry_point("analyst")

graph.add_edge("analyst", "requirements")
graph.add_edge("requirements", "srs")
graph.add_edge("srs", "architecture")
graph.add_edge("architecture", "qa")
graph.add_edge("qa", "save")
graph.add_edge("save", END)

workflow = graph.compile()


# -----------------------------------
# REUSABLE FUNCTION
# -----------------------------------

def run_workflow(project_name):

    result = workflow.invoke(
        {
            "project": project_name
        }
    )

    return result


# -----------------------------------
# EXECUTION
# -----------------------------------

if __name__ == "__main__":

    project_name = input(
        "\nEnter Project Name: "
    )

    try:

        result = run_workflow(project_name)

        print("\n")
        print("=" * 80)
        print("BUSINESS ANALYSIS")
        print("=" * 80)
        print(result["analysis"])

        print("\n")
        print("=" * 80)
        print("REQUIREMENTS")
        print("=" * 80)
        print(result["requirements"])

        print("\n")
        print("=" * 80)
        print("SRS DOCUMENT")
        print("=" * 80)
        print(result["srs"])

        print("\n")
        print("=" * 80)
        print("SYSTEM ARCHITECTURE")
        print("=" * 80)
        print(result["architecture"])

        print("\n")
        print("=" * 80)
        print("TEST CASES")
        print("=" * 80)
        print(result["tests"])

        print("\n")
        print("=" * 80)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 80)

    except Exception as e:

        print("\nERROR OCCURRED")
        print(str(e))