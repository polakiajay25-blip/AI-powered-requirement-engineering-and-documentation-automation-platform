from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "faiss_db",
    embedding,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever()

def get_context(query):

    docs = retriever.invoke(query)

    return "\n".join(
        [doc.page_content for doc in docs]
    )