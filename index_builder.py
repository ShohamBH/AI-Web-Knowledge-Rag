import logging
from llama_index.core import VectorStoreIndex

logger = logging.getLogger(__name__)

def build_index(documents):
    """בנה Vector Store Index מ-documents"""
    try:
        logger.info(f"🔨 Building index from {len(documents)} documents...")
        index = VectorStoreIndex.from_documents(documents)
        logger.info("✅ Index built successfully")
        return index
    except Exception as e:
        logger.error(f"❌ Error building index: {str(e)}")
        return None
