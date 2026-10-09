# AI-Powered Requirement Engineering and Documentation Automation Platform

An AI-powered software engineering platform that automates requirement analysis, software documentation generation, architecture design, and quality analysis using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and a multi-agent architecture.

## 📌 Project Overview

Software development requires clear requirements, structured documentation, proper architecture planning, and quality validation. Preparing these deliverables manually can be time-consuming and may lead to inconsistencies.

The **AI-Powered Requirement Engineering and Documentation Automation Platform** aims to simplify this process by using AI agents to analyze project ideas and generate structured software engineering deliverables.

The platform uses LangGraph to organize agent workflows, Ollama to run a local language model, and FAISS to retrieve relevant information from project documents. A Streamlit interface allows users to interact with the system, while FastAPI provides backend API functionality.

## 🎯 Objectives

* Automate software requirement analysis from project descriptions.
* Generate structured software requirements and documentation.
* Assist in software architecture design.
* Analyze generated outputs for quality and consistency.
* Retrieve relevant information from reference documents using RAG.
* Maintain project details and generation history.
* Provide a simple and interactive user interface.

## ✨ Key Features

### 1. Requirement Analysis

Analyzes the user's project idea and helps identify the main requirements and system functionality.

### 2. Software Documentation Generation

Generates structured software documentation based on the provided project description and requirements.

### 3. Architecture Design

Assists in identifying system components and preparing a high-level software architecture.

### 4. AI-Based Quality Analysis

Evaluates generated requirements and documentation for clarity, completeness, and consistency, depending on the implemented checks.

### 5. Retrieval-Augmented Generation (RAG)

Uses FAISS to retrieve relevant information from a collection of reference documents to support context-aware generation.

### 6. Multi-Agent Workflow

Uses LangGraph to organize specialized agents for requirement analysis, documentation, architecture design, and quality analysis.

### 7. Project History

Uses SQLite to store project information and support access to previously generated content.

### 8. Interactive User Interface

Provides a Streamlit frontend for entering project ideas, viewing generated results, and interacting with the platform.

### 9. Backend API

Uses FastAPI to expose backend functionality through API endpoints.

## 🏗️ System Architecture

The platform follows a modular architecture consisting of the following components:

1. **User Interface — Streamlit:** Accepts project descriptions and displays generated outputs.
2. **Backend API — FastAPI:** Handles application requests and backend operations.
3. **Agent Orchestration — LangGraph:** Coordinates the workflow between specialized agents.
4. **Language Model — Ollama:** Runs the configured local LLM for text generation.
5. **Knowledge Retrieval — FAISS:** Retrieves relevant information from indexed reference documents.
6. **Data Storage — SQLite:** Stores project information and generation history.

### Workflow

```text
        User Project Idea
                |
                v
        Streamlit Frontend
                |
                v
          FastAPI Backend
                |
                v
       LangGraph Orchestrator
                |
       +--------+---------+
       |        |         |
       v        v         v
  Requirement Documentation Architecture
    Agent       Agent       Agent
       |        |         |
       +--------+---------+
                |
                v
        Quality Analysis Agent
                |
                v
        Generated Deliverables
                |
        +-------+--------+
        |                |
        v                v
   Streamlit UI      SQLite History

     FAISS Retrieval + Ollama LLM
       support the agent workflow
```

*Note: This diagram represents the intended logical workflow. The exact execution order and integrations depend on the implemented application code.*

## 🛠️ Technologies Used

| Technology            | Purpose                                    |
| --------------------- | ------------------------------------------ |
| Python                | Core programming language                  |
| LangChain             | LLM integration and application components |
| LangGraph             | Agent workflow orchestration               |
| Ollama                | Local language model execution             |
| Llama 3.2             | Configured language model                  |
| FAISS                 | Vector similarity search                   |
| FastAPI               | Backend API development                    |
| Streamlit             | Interactive frontend                       |
| SQLite                | Project data storage                       |
| Sentence Transformers | Text embeddings                            |
| PyPDF                 | PDF document processing                    |

## 📂 Project Structure

```text
AI_Requirement_Platform/
│
├── agents/
│   ├── analyst_agent.py
│   ├── requirement_agent.py
│   ├── documentation_agent.py
│   ├── architecture_agent.py
│   └── qa_agent.py
│
├── backend/
│   └── api.py
│
├── rag/
│   ├── vector_store.py
│   └── retriever.py
│
├── app/
│   └── streamlit_app.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

*The structure above is representative. Update it to match the files and folders in your actual repository.*

## ⚙️ Installation and Setup

### Prerequisites

* Python 3.10 or a compatible version supported by your dependencies
* Git
* Ollama
* VS Code or another Python IDE

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Requirement-Engineering-Platform.git
cd AI-Requirement-Engineering-Platform
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
python -m venv myenv
```

Activate it on Windows PowerShell:

```powershell
.\myenv\Scripts\Activate.ps1
```

### 3. Install Dependencies

If your repository contains `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the dependencies listed in your project configuration.

### 4. Set Up Ollama

Install Ollama from the official website:

https://ollama.com/

Download the configured model:

```bash
ollama pull llama3.2
```

Ensure Ollama is running before starting the application.

### 5. Run the Application

If your Streamlit entry point is `app/streamlit_app.py`, run:

```bash
streamlit run app/streamlit_app.py
```

If you want to run the FastAPI backend separately, use:

```bash
uvicorn backend.api:app --reload
```

The actual startup commands may need adjustment based on your current application configuration.

## 🧪 Example Use Case

**Input:** An online pharmacy management system.

The platform can assist with preparing:

* Functional and non-functional requirements.
* Structured software documentation.
* High-level architecture descriptions.
* Quality review suggestions.
* Relevant context retrieved from reference documents.

The actual output depends on the implemented agents, prompts, and available reference data.

## 🔮 Future Enhancements

* Export generated deliverables to PDF and DOCX.
* Add requirement traceability and change-impact analysis.
* Include automated acceptance-test generation.
* Improve requirement completeness and consistency scoring.
* Add user authentication and role-based access control.
* Support additional local and cloud-based language models.
* Add evaluation datasets and measurable quality benchmarks.
* Improve architecture diagrams and documentation templates.

## 🎓 Project Applications

* Software requirement engineering.
* Automated technical documentation.
* Early-stage software architecture planning.
* AI-assisted software development.
* Academic and prototype software engineering projects.

## 👨‍💻 Project Information

**Project Title:** AI-Powered Requirement Engineering and Documentation Automation Platform

**Domain:** Artificial Intelligence, Natural Language Processing, and Software Engineering

**Project Type:** Final-Year Academic Project

**Primary Language:** Python

## 📄 License

Choose an appropriate open-source license before distributing this project publicly. Until a license is added, the repository is not automatically granted an open-source license.

## ⭐ Acknowledgements

This project explores the application of open-source language models, retrieval systems, and agent-based workflows to improve software requirement engineering and documentation processes.
