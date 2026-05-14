import logging
from config import SIMILARITY_TOP_K

logger = logging.getLogger(__name__)

def generate_tiered_summary(index):
    """Feature 1: סיכום חכם מדורג (TL;DR, בינוני, עמוק)"""
    try:
        logger.info("📋 Generating tiered summary...")
        qe = index.as_query_engine(similarity_top_k=SIMILARITY_TOP_K)
        
        tldr = qe.query("Provide a concise 1-sentence summary. Ensure complete sentence.")
        medium = qe.query("Write a 1-paragraph summary with complete sentences.")
        deep = qe.query("Provide detailed summary with bullet points for each main section.")
        
        return {
            "TLDR": str(tldr),
            "Medium": str(medium),
            "Deep": str(deep)
        }
    except Exception as e:
        logger.error(f"❌ Error generating summary: {str(e)}")
        return None

def smart_navigation(index, documents):
    """Feature 3: ניווט חכם במאמר - מחזיר סעיפים עם הסברים"""
    try:
        logger.info("🧭 Generating smart navigation...")
        qe = index.as_query_engine(similarity_top_k=SIMILARITY_TOP_K)
        
        navigation = []
        for doc in documents:
            section_title = doc.metadata.get("section", "Unknown")
            section_index = doc.metadata.get("section_index", 0)
            
            # קבל הסבר קצר לסעיף
            explanation = qe.query(f"Explain this section in 2-3 sentences: {section_title}")
            
            navigation.append({
                "index": section_index,
                "title": section_title,
                "content_preview": doc.text[:200] + "...",
                "explanation": str(explanation)
            })
        
        return sorted(navigation, key=lambda x: x["index"])
    except Exception as e:
        logger.error(f"❌ Error generating navigation: {str(e)}")
        return None

def generate_study_material(index):
    """Feature 4: מצב לימוד - flashcards וקוויז"""
    try:
        logger.info("📚 Generating study material...")
        qe = index.as_query_engine(similarity_top_k=SIMILARITY_TOP_K)
        
        # Generate flashcards
        fc_response = qe.query(
            "Generate 5 unique flashcards in this format:\n"
            "Q1: [question]\nA1: [answer]\n\n"
            "Q2: [question]\nA2: [answer]\n\n"
            "Make them diverse and interesting."
        )
        
        # Generate quiz
        quiz_response = qe.query(
            "Generate 3 unique multiple-choice questions with A,B,C,D options and correct answer.\n"
            "Format:\nQuestion 1: [question]\nA) [option]\nB) [option]\nC) [option]\nD) [option]\nCorrect: [letter]\n\n"
            "Only use explicit content from the page."
        )
        
        # Parse flashcards
        flashcards = parse_flashcards(str(fc_response))
        
        return {
            "flashcards": flashcards[:5],
            "quiz": str(quiz_response)
        }
    except Exception as e:
        logger.error(f"❌ Error generating study material: {str(e)}")
        return None

def parse_flashcards(text: str) -> list:
    """Parse flashcards from text"""
    flashcards = []
    pairs = text.split('\n\n')
    
    for pair in pairs:
        lines = pair.strip().split('\n')
        question = None
        answer = None
        
        for line in lines:
            if line.startswith('Q') and ':' in line:
                question = line.split(':', 1)[1].strip()
            elif line.startswith('A') and ':' in line:
                answer = line.split(':', 1)[1].strip()
        
        if question and answer:
            flashcards.append({"question": question, "answer": answer})
    
    return flashcards

def answer_question(index, question: str):
    """Feature 2: RAG Engine - שאלות ותשובות"""
    try:
        logger.info(f"❓ Answering question: {question}")
        qe = index.as_query_engine(similarity_top_k=SIMILARITY_TOP_K)
        response = qe.query(question)
        
        sources = []
        if hasattr(response, 'source_nodes') and response.source_nodes:
            for node in response.source_nodes:
                content = node.get_content()[:150]
                section = node.metadata.get("section", "Unknown")
                sources.append({"section": section, "content": content})
        
        return {
            "answer": str(response),
            "sources": sources
        }
    except Exception as e:
        logger.error(f"❌ Error answering question: {str(e)}")
        return None
