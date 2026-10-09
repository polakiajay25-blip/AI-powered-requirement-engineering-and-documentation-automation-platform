from rag.retriever import get_context

query = "hospital patient records"

context = get_context(query)

print(context)