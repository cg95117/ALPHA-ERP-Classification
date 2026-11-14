# ==============================================================================
# index_setup.py
# Builds the ChromaDB index from the human-labelled training data.
# Run once initially, or again when the training data changes.
# To rebuild from scratch, delete the chroma_db/ folder first.
# ==============================================================================
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from src.load_data import load_training_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

training_data = load_training_data()
documents = []

for index, row in training_data.iterrows():
    documents.append(
        Document(
            page_content=row["Text"],
            metadata={
                "category": row["Category"],
                "reason": row["Reason"],
                "excel_row": int(index + 2),
            },
        )
    )

database = Chroma.from_documents(
    documents=documents,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="training_data",
    persist_directory=str(CHROMA_DIR),
    collection_metadata={"hnsw:space": "cosine"},
)

print("Stored documents:", len(database.get()["ids"]))
