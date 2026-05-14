#!/usr/bin/env python3
"""
בדיקת הפרויקט - וודא שכל המודולים עובדים
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """בדוק שכל ה-imports עובדים"""
    logger.info("🔍 Testing imports...")
    
    try:
        import config
        logger.info("✅ config.py")
    except Exception as e:
        logger.error(f"❌ config.py: {str(e)}")
        return False
    
    try:
        import web_scraper
        logger.info("✅ web_scraper.py")
    except Exception as e:
        logger.error(f"❌ web_scraper.py: {str(e)}")
        return False
    
    try:
        import index_builder
        logger.info("✅ index_builder.py")
    except Exception as e:
        logger.error(f"❌ index_builder.py: {str(e)}")
        return False
    
    try:
        import features
        logger.info("✅ features.py")
    except Exception as e:
        logger.error(f"❌ features.py: {str(e)}")
        return False
    
    try:
        import ui
        logger.info("✅ ui.py")
    except Exception as e:
        logger.error(f"❌ ui.py: {str(e)}")
        return False
    
    return True

def test_config():
    """בדוק הגדרות"""
    logger.info("\n🔧 Testing config...")
    
    try:
        from config import CHUNK_SIZE, CHUNK_OVERLAP, SIMILARITY_TOP_K, MIN_CONTENT_LENGTH
        logger.info(f"✅ Constants loaded: CHUNK_SIZE={CHUNK_SIZE}, CHUNK_OVERLAP={CHUNK_OVERLAP}, SIMILARITY_TOP_K={SIMILARITY_TOP_K}, MIN_CONTENT_LENGTH={MIN_CONTENT_LENGTH}")
        return True
    except Exception as e:
        logger.error(f"❌ Config error: {str(e)}")
        return False

def test_env():
    """בדוק משתנים סביבה"""
    logger.info("\n🔐 Testing environment variables...")
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_keys = {
        "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY"),
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY"),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
    }
    
    has_key = False
    for key, value in api_keys.items():
        if value:
            logger.info(f"✅ {key} is set")
            has_key = True
        else:
            logger.warning(f"⚠️ {key} is not set")
    
    if not has_key:
        logger.error("❌ No API keys found! Set at least one in .env")
        return False
    
    return True

def main():
    logger.info("=" * 50)
    logger.info("🚀 AI Web Knowledge Summarizer - Test Suite")
    logger.info("=" * 50)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Config", test_config()))
    results.append(("Environment", test_env()))
    
    logger.info("\n" + "=" * 50)
    logger.info("📊 Test Results:")
    logger.info("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        logger.info("\n✅ All tests passed! You can run: streamlit run app_new.py")
        return 0
    else:
        logger.error("\n❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
