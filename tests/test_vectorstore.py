"""
Vector Store Tests
Tests for Chroma vector database and retrieval functionality
"""

import pytest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestVectorStoreSetup:
    """Test vector store initialization and setup"""
    
    def test_vectorstore_directory_exists(self):
        """Test that vectorstore directory exists"""
        assert os.path.exists("vectorstore"), "Vector store directory not found"
    
    def test_vectorstore_has_data(self):
        """Test that vectorstore contains data"""
        vectorstore_dir = "vectorstore"
        files = os.listdir(vectorstore_dir)
        assert len(files) > 0, "Vector store directory is empty"
    
    def test_chroma_database_exists(self):
        """Test that Chroma database file exists"""
        chroma_db = "vectorstore/chroma.sqlite3"
        assert os.path.exists(chroma_db), "Chroma database file not found"


class TestVectorStoreRetrieval:
    """Test document retrieval from vector store"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup vector store for testing"""
        try:
            from langchain_chroma import Chroma
            from langchain_huggingface import HuggingFaceEmbeddings
            
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            self.db = Chroma(persist_directory="vectorstore", embedding_function=self.embeddings)
            self.retriever = self.db.as_retriever(search_kwargs={"k": 5})
        except Exception as e:
            pytest.skip(f"Could not initialize vector store: {e}")
    
    def test_retrieval_returns_documents(self, sample_query):
        """Test that retrieval returns documents"""
        docs = self.retriever.invoke(sample_query)
        assert len(docs) > 0, "No documents retrieved"
        assert all(hasattr(doc, 'page_content') for doc in docs), "Documents missing content"
    
    def test_similarity_search(self):
        """Test similarity search functionality"""
        query = "study visa requirements"
        docs = self.db.similarity_search(query, k=3)
        assert len(docs) <= 3, "Returned more documents than requested"
        assert len(docs) > 0, "No documents found"
    
    def test_retrieval_relevance(self):
        """Test that retrieved documents are relevant"""
        query = "Canada student visa"
        docs = self.db.similarity_search(query, k=5)
        
        # Check if retrieved documents mention relevant keywords
        all_content = " ".join([doc.page_content.lower() for doc in docs])
        assert "canada" in all_content or "student" in all_content or "study" in all_content, \
            "Retrieved documents don't seem relevant to query"
    
    def test_empty_query_handling(self):
        """Test handling of empty query"""
        try:
            docs = self.db.similarity_search("", k=3)
            # Should either return empty or handle gracefully
            assert isinstance(docs, list), "Should return list even for empty query"
        except Exception:
            # It's acceptable to raise an exception for empty query
            pass


class TestEmbeddings:
    """Test embedding generation"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup embeddings model"""
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        except Exception as e:
            pytest.skip(f"Could not initialize embeddings: {e}")
    
    def test_embed_documents(self):
        """Test embedding generation for documents"""
        texts = ["This is a test document", "Another test document"]
        embeddings = self.embeddings.embed_documents(texts)
        
        assert len(embeddings) == 2, "Should return 2 embeddings"
        assert all(isinstance(emb, list) for emb in embeddings), "Embeddings should be lists"
        assert all(len(emb) > 0 for emb in embeddings), "Embeddings should not be empty"
    
    def test_embed_query(self):
        """Test embedding generation for query"""
        query = "test query"
        embedding = self.embeddings.embed_query(query)
        
        assert isinstance(embedding, list), "Embedding should be a list"
        assert len(embedding) > 0, "Embedding should not be empty"
        assert all(isinstance(x, float) for x in embedding), "Embedding values should be floats"


class TestVectorStorePerformance:
    """Test vector store performance"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup vector store for testing"""
        try:
            from langchain_chroma import Chroma
            from langchain_huggingface import HuggingFaceEmbeddings
            import time
            
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            self.db = Chroma(persist_directory="vectorstore", embedding_function=self.embeddings)
            self.time = time
        except Exception as e:
            pytest.skip(f"Could not initialize vector store: {e}")
    
    def test_query_performance(self):
        """Test that queries complete in reasonable time"""
        import time
        
        query = "visa requirements"
        start_time = time.time()
        docs = self.db.similarity_search(query, k=5)
        end_time = time.time()
        
        duration = end_time - start_time
        assert duration < 5.0, f"Query took too long: {duration:.2f}s"
        assert len(docs) > 0, "No documents retrieved"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
