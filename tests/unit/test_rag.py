import pytest
from app.rag.ingestion import DocumentIngestionPipeline
from app.rag.embeddings import MockEmbeddingModel, cosine_similarity
from app.rag.reranker import ContextReranker
from app.rag.retrieval import RAGRetrievalPipeline


def test_document_ingestion_chunking():
    pipeline = DocumentIngestionPipeline(chunk_size=10, chunk_overlap=2)
    raw_doc = {
        "document_id": "TEST_DOC",
        "title": "Test Policy",
        "department": "compliance",
        "content": "Word " * 35
    }
    chunks = pipeline.chunk_document(raw_doc)
    assert len(chunks) > 1
    assert chunks[0].document_id == "TEST_DOC"


def test_embedding_model_and_cosine_similarity():
    model = MockEmbeddingModel(dimension=64)
    v1 = model.embed_query("suspicious money laundering transaction")
    v2 = model.embed_query("suspicious transaction wire")
    v3 = model.embed_query("completely unrelated recipe for chocolate cake")

    sim_high = cosine_similarity(v1, v2)
    sim_low = cosine_similarity(v1, v3)
    assert sim_high > sim_low


@pytest.mark.asyncio
async def test_rag_retrieval_pipeline():
    rag = RAGRetrievalPipeline()
    citations = await rag.search(query="suspicious transaction SAR reporting", top_k=2)

    assert len(citations) > 0
    assert citations[0].relevance_score > 0.0
    assert "document_id" in citations[0].model_dump()
    assert citations[0].metadata["sensitivity"] == "confidential"
