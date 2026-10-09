import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load all text documents
documents = []

docs_folder = "documents"

for file in os.listdir(docs_folder):
    if file.endswith(".txt"):

        filepath = os.path.join(
            docs_folder,
            file
        )

        loader = TextLoader(
            filepath,
            encoding="utf-8"
        )

        documents.extend(
            loader.load()
        )

print(f"Loaded {len(documents)} documents")

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

docs = splitter.split_documents(
    documents
)

print(f"Created {len(docs)} chunks")

# Create embeddings
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create FAISS vector store
vectorstore = FAISS.from_documents(
    docs,
    embedding
)

# Save locally
vectorstore.save_local("faiss_db")

print("FAISS database created successfully!")