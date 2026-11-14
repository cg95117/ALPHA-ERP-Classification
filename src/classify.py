# ==============================================================================
# classify.py
# Assigns one or more ERP technology categories to a coding unit using an LLM.
# Prerequisites: index_setup.py has been run and Ollama/models are available.
# ==============================================================================
from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

from src.load_data import load_categories, load_test_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

database = Chroma(
    collection_name="training_data",
    persist_directory=str(CHROMA_DIR),
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
)

llm = ChatOllama(model="qwen3:14b", temperature=0)
MAX_DISTANCE = 0.230


def categories_as_text():
    lines = []
    for _, category in load_categories().iterrows():
        lines.append(
            category["Category"] + ": "
            + category["Technology"] + " - "
            + category["Description"]
        )
    return "\\n".join(lines)


def examples_as_text(results):
    lines = []
    for document in results:
        lines.append("Category: " + document.metadata["category"])
        lines.append("Text: " + document.page_content)
        lines.append("Reason: " + document.metadata["reason"])
        lines.append("")
    return "\\n".join(lines)


def classify(text):
    """Classify one text and return the model response plus retrieved examples."""
    results_with_distance = database.similarity_search_with_score(text, k=5)
    results = [
        document
        for document, distance in results_with_distance
        if distance <= MAX_DISTANCE
    ]

    prompt = (
        "You assign text excerpts from technical literature on ERP systems to a category.\\n\\n"
        "CATEGORY SYSTEM\\n" + categories_as_text() + "\\n\\n"
        "SIMILAR EXAMPLES ALREADY ASSIGNED\\n" + examples_as_text(results) + "\\n"
        "NEW TEXT\\n" + text + "\\n\\n"
        "Select the appropriate category as a letter. Separate multiple categories with commas. "
        "If no technology is apparent, answer with X.\\n"
        "Answer exactly in this format:\\n"
        "Category: <Letter>\\n"
        "Reason: <one to two sentences in English>\\n"
        "If multiple categories are selected, give a separate justification for each category "
        "in the same line, for example, Q: <justification>; L: <justification>."
    )
    response = llm.invoke(prompt)
    return response.content, results


if __name__ == "__main__":
    text = load_test_data()["Coding_Unit"].iloc[0]
    result, results = classify(text)
    print("NEW TEXT:", text)
    print("\\nRETRIEVED EXAMPLES:")
    for document in results:
        print("  [" + document.metadata["category"] + "]", document.page_content[:80])
    print("\\n" + result)
