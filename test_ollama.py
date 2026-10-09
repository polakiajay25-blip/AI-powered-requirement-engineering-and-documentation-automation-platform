from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2")

response = llm.invoke(
    "Generate requirements for a Library Management System"
)

print(response)