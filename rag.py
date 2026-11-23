from pathlib import Path

from cosine_similarity import cosine_similarity
from get_vector_embedding import get_embedding


DOCS_DIR = Path(__file__).resolve().parent / "docs"
_document_chunks = None
_chunk_embeddings = None


def load_documents(docs_dir=DOCS_DIR):
    """Load and chunk all text documents in a folder."""
    chunks = []

    for path in sorted(Path(docs_dir).glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue

        title = text.splitlines()[0].strip()
        paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]

        for index, paragraph in enumerate(paragraphs):
            chunks.append({
                "source": path.name,
                "title": title,
                "chunk_index": index,
                "text": paragraph,
            })

    return chunks


def _get_rag_data():
    """Load documents and calculate embeddings once."""
    global _document_chunks, _chunk_embeddings

    if _document_chunks is None:
        _document_chunks = load_documents()

    if _chunk_embeddings is None:
        _chunk_embeddings = [
            get_embedding(chunk["text"])
            for chunk in _document_chunks
        ]

    return _document_chunks, _chunk_embeddings


def search(query, top_k=3):
    """Find the most relevant company document chunks for a query."""
    if not query or not isinstance(query, str):
        return "Search query must be a non-empty string."

    top_k = max(1, min(int(top_k), 10))

    try:
        chunks, chunk_embeddings = _get_rag_data()
        if not chunks:
            return "No company documents are available."

        query_embedding = get_embedding(query)
        ranked = sorted(
            (
                (cosine_similarity(query_embedding, embedding), chunk)
                for chunk, embedding in zip(chunks, chunk_embeddings)
            ),
            key=lambda item: item[0],
            reverse=True,
        )

        results = []
        for score, chunk in ranked[:top_k]:
            results.append(
                f"[Source: {chunk['source']} | Relevance: {score:.3f}]\n"
                f"{chunk['text']}"
            )

        return "\n\n".join(results)
    except Exception as exc:
        return f"Unable to search company documents: {exc}"
