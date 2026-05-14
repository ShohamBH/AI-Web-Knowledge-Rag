import os
import logging
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# קבועים
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
SIMILARITY_TOP_K = 5
MIN_CONTENT_LENGTH = 200

# Embedding Model
EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"

def initialize_llm():
    """אתחול LLM עם fallback logic"""
    llm = None
    provider = None
    
    try:
        logger.info("⏳ Trying Gemini...")
        from llama_index.llms.gemini import Gemini
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key:
            llm = Gemini(model="gemini-1.5-flash", api_key=api_key)
            logger.info("✅ Gemini loaded")
            provider = "Gemini"
    except Exception as e:
        logger.warning(f"⚠️ Gemini failed: {str(e)}")
    
    if not provider:
        try:
            logger.info("⏳ Trying Groq...")
            from llama_index.llms.groq import Groq
            api_key = os.environ.get("GROQ_API_KEY")
            if api_key:
                llm = Groq(model="llama-3.1-8b-instant", api_key=api_key)
                logger.info("✅ Groq loaded")
                provider = "Groq"
        except Exception as e:
            logger.warning(f"⚠️ Groq failed: {str(e)}")
    
    if not provider:
        try:
            logger.info("⏳ Trying OpenAI...")
            from llama_index.llms.openai import OpenAI
            api_key = os.environ.get("OPENAI_API_KEY")
            if api_key:
                llm = OpenAI(model="gpt-4o-mini", api_key=api_key)
                logger.info("✅ OpenAI loaded")
                provider = "OpenAI"
        except Exception as e:
            logger.warning(f"⚠️ OpenAI failed: {str(e)}")
    
    if not provider:
        raise RuntimeError("❌ No LLM provider available. Set GOOGLE_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY")
    
    return llm, provider

def setup_settings():
    """הגדרת LlamaIndex Settings"""
    llm, provider = initialize_llm()
    embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
    text_splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.text_splitter = text_splitter
    
    return llm, embed_model, provider
