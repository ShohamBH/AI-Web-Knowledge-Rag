import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from llama_index.core import Document
from config import MIN_CONTENT_LENGTH

logger = logging.getLogger(__name__)

try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except ImportError:
    HAS_CLOUDSCRAPER = False

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
]

HEADERS_BASE = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def fetch_html(url: str) -> str:
    """טעינת HTML מ-URL עם fallback logic"""
    html = None
    
    if HAS_CLOUDSCRAPER:
        try:
            logger.info("⏳ Trying cloudscraper...")
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Cloudscraper success")
                return response.text
        except Exception as e:
            logger.warning(f"⚠️ Cloudscraper failed: {str(e)}")
    
    logger.info("⏳ Trying requests with multiple user agents...")
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    
    for ua in USER_AGENTS:
        try:
            with requests.Session() as session:
                session.mount("http://", adapter)
                session.mount("https://", adapter)
                headers = HEADERS_BASE.copy()
                headers['User-Agent'] = ua
                response = session.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    logger.info("✅ Requests success")
                    return response.text
        except Exception as e:
            logger.warning(f"⚠️ User agent {ua[:30]}... failed: {str(e)}")
            continue
    
    return None

def extract_sections(soup) -> list:
    """חלץ סעיפים עם כותרות מהדף"""
    sections = []
    current_section = {"title": "Introduction", "content": ""}
    
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
        if element.name in ['h1', 'h2', 'h3']:
            if current_section["content"].strip():
                sections.append(current_section)
            current_section = {"title": element.get_text().strip(), "content": ""}
        elif element.name in ['p', 'li']:
            current_section["content"] += element.get_text().strip() + "\n"
    
    if current_section["content"].strip():
        sections.append(current_section)
    
    return sections

def load_web_data(url: str) -> list:
    """טעינת תוכן מאתר וחלוקה לסעיפים"""
    logger.info(f"📥 Loading URL: {url}")
    
    html = fetch_html(url)
    if not html:
        return None
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # חלץ כותרת
        title_tag = soup.find('title')
        page_title = title_tag.get_text().strip() if title_tag else "Unknown Title"
        
        # הסר אלמנטים לא רלוונטיים
        for tag in ['nav', 'footer', 'script', 'style', 'noscript', 'header', 'aside', 'form', 'button']:
            for el in soup.find_all(tag):
                el.decompose()
        
        # חלץ תוכן ראשי
        main = soup.find('main') or soup.find('article') or soup.body
        if not main:
            return None
        
        # חלץ סעיפים
        sections = extract_sections(main)
        
        if not sections:
            return None
        
        # בנה Documents
        documents = []
        for i, section in enumerate(sections):
            if len(section["content"].strip()) > 50:
                doc = Document(
                    text=section["content"],
                    metadata={
                        "source": url,
                        "title": page_title,
                        "section": section["title"],
                        "section_index": i
                    }
                )
                documents.append(doc)
        
        if not documents:
            return None
        
        # בדוק אם יש מספיק תוכן
        total_length = sum(len(doc.text) for doc in documents)
        if total_length < MIN_CONTENT_LENGTH:
            logger.error(f"❌ Content too short: {total_length} chars")
            return None
        
        logger.info(f"✅ Loaded {len(documents)} sections, {total_length} chars total")
        return documents
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return None
