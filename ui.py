import streamlit as st
from datetime import datetime

def setup_page():
    """הגדרת עמוד Streamlit"""
    st.set_page_config(
        page_title="AI Web Knowledge Summarizer",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
        <style>
        .main-header { font-size: 3rem; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; text-align: center; }
        .subtitle { font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem; }
        .url-section { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; color: white; }
        .url-section h2 { color: white; margin-top: 0; }
        .status-badge { display: inline-block; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: bold; margin: 0.5rem 0; }
        .status-success { background: #d4edda; color: #155724; }
        .footer { text-align: center; color: #999; font-size: 0.9rem; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #eee; }
        .tldr-box { background: white; border: 2px solid #10b981; padding: 2rem; border-radius: 1rem; margin: 1.5rem 0; border-left: 5px solid #047857; }
        .tldr-box strong { color: #10b981; font-size: 1.3rem; display: block; margin-bottom: 1rem; }
        .medium-box { background: white; border: 2px solid #f59e0b; padding: 2rem; border-radius: 1rem; margin: 1.5rem 0; border-left: 5px solid #b45309; }
        .medium-box strong { color: #f59e0b; font-size: 1.2rem; display: block; margin-bottom: 1rem; }
        .deep-box { background: white; border: 2px solid #ef4444; padding: 2rem; border-radius: 1rem; margin: 1.5rem 0; border-left: 5px solid #b91c1c; }
        .deep-box strong { color: #ef4444; font-size: 1.2rem; display: block; margin-bottom: 1rem; }
        .question-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 0.8rem; margin: 1rem 0; font-size: 1.1rem; font-weight: 500; }
        .answer-box { background: #f0f4ff; border-left: 4px solid #667eea; padding: 1.5rem; border-radius: 0.8rem; margin: 0.5rem 0 1.5rem 0; font-size: 1rem; }
        .quiz-question-container { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 1rem; margin: 2rem 0 1rem 0; border-left: 5px solid #5568d3; }
        .quiz-question-container strong { font-size: 1.2rem; display: block; margin-bottom: 1rem; }
        .quiz-option-item { background: #f8f9fa; border: 2px solid #e0e0e0; padding: 1rem; margin: 0.8rem 0; border-radius: 0.5rem; font-size: 1rem; }
        .quiz-answer { background: #d4edda; border-left: 4px solid #28a745; padding: 1rem; margin: 1rem 0 2rem 0; border-radius: 0.5rem; color: #155724; font-weight: 500; }
        .source-item { padding: 0.5rem 0; font-size: 0.85rem; color: #666; border-bottom: 1px solid #eee; }
        .nav-item { background: #f8f9fa; border-left: 4px solid #667eea; padding: 1rem; margin: 0.8rem 0; border-radius: 0.5rem; }
        .nav-item-title { font-weight: bold; color: #667eea; margin-bottom: 0.5rem; }
        .stTabs [data-baseweb="tab-list"] button { font-size: 1.3rem !important; padding: 1rem !important; }
        </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """אתחול session state"""
    if "index" not in st.session_state:
        st.session_state.index = None
    if "current_url" not in st.session_state:
        st.session_state.current_url = None
    if "documents" not in st.session_state:
        st.session_state.documents = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "summaries" not in st.session_state:
        st.session_state.summaries = None
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = None
    if "quiz" not in st.session_state:
        st.session_state.quiz = None
    if "navigation" not in st.session_state:
        st.session_state.navigation = None

def render_header(provider):
    """הצג כותרת"""
    st.markdown('<div class="main-header">🚀 AI Web Knowledge Summarizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Analyze webpages with AI summaries, Q&A, and study materials</div>', unsafe_allow_html=True)
    st.info(f"🤖 Using: **{provider}**")

def render_url_input():
    """הצג קלט URL"""
    st.markdown('<div class="url-section">', unsafe_allow_html=True)
    st.markdown("### 📍 Enter a URL")
    col1, col2 = st.columns([4, 1])
    with col1:
        url_input = st.text_input("URL:", placeholder="https://example.com", label_visibility="collapsed")
    with col2:
        analyze_button = st.button("🚀 Analyze", use_container_width=True, key="analyze_btn")
    st.markdown('</div>', unsafe_allow_html=True)
    
    return url_input, analyze_button

def render_welcome():
    """הצג עמוד ברוכים הבאים"""
    st.info("👆 Enter URL and click Analyze!")
    st.markdown("""
    ### 📖 How to use:
    
    1. **Paste a URL** (e.g., Wikipedia, blog posts, documentation)
    2. **Click 'Analyze'** to scrape and process the content
    3. **View Summaries** - Get TL;DR, Medium, and Deep summaries
    4. **Ask Questions** - Use RAG to ask questions about the content
    5. **Study** - Generate flashcards and quizzes for learning
    6. **Navigate** - Explore the article structure with smart navigation
    
    ### ✨ Features:
    - 🎯 Multi-level summaries (TL;DR, Medium, Deep)
    - 💬 Interactive Q&A with source tracking
    - 📚 Auto-generated flashcards and quizzes
    - 🧭 Smart navigation through article sections
    - ⚡ Multi-provider LLM support (Gemini → Groq → OpenAI)
    
    ### 🔧 Technologies:
    - **LLaMA Index** - RAG framework
    - **HuggingFace Embeddings** - BAAI/bge-small-en-v1.5
    - **Streamlit** - Web UI
    - **BeautifulSoup** - Web scraping
    - **Cloudscraper** - Bypass bot detection
    """)

def render_summary_tab(generate_summary_callback, export_callback):
    """הצג טאב סיכומים"""
    st.title("📋 Summary")
    if st.session_state.summaries is None:
        if st.button("Generate", use_container_width=True, key="gen_summary"):
            with st.spinner("⏳ Generating..."):
                generate_summary_callback()
    else:
        st.success("✅ Generated")
        st.markdown(f'<div class="tldr-box"><strong>🟢 TL;DR</strong>{st.session_state.summaries["TLDR"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="medium-box"><strong>🟡 Medium</strong>{st.session_state.summaries["Medium"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="deep-box"><strong>🔴 Deep</strong>{st.session_state.summaries["Deep"]}</div>', unsafe_allow_html=True)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Regenerate", use_container_width=True, key="regen_summary"):
                st.session_state.summaries = None
                st.rerun()
        with col2:
            st.download_button("📥 Export", export_callback(), f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", "text/markdown", use_container_width=True, key="export_summary")
        with col3:
            if st.button("🗑️ Clear All", use_container_width=True, key="clear_all"):
                st.session_state.summaries = None
                st.session_state.flashcards = None
                st.session_state.quiz = None
                st.session_state.navigation = None
                st.session_state.chat_history = []
                st.rerun()

def render_chat_tab(answer_question_callback):
    """הצג טאב צ'אט"""
    st.title("💬 Chat")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "sources" in msg:
                with st.expander("📍 Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"<div class='source-item'>📌 **{src['section']}**: {src['content']}...</div>", unsafe_allow_html=True)
    
    q = st.chat_input("Ask...")
    if q:
        st.session_state.chat_history.append({"role": "user", "content": q})
        with st.chat_message("user"):
            st.markdown(q)
        
        with st.spinner("🤖 Thinking..."):
            result = answer_question_callback(q)
            if result:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"]
                })
                with st.chat_message("assistant"):
                    st.markdown(result["answer"])
                    if result["sources"]:
                        with st.expander("📍 Sources"):
                            for src in result["sources"]:
                                st.markdown(f"<div class='source-item'>📌 **{src['section']}**: {src['content']}...</div>", unsafe_allow_html=True)
                st.rerun()
    
    if st.button("🗑️ Clear", use_container_width=True, key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

def render_study_tab(generate_study_callback, export_callback):
    """הצג טאב לימוד"""
    st.title("📚 Study")
    if st.session_state.flashcards is None:
        if st.button("Generate", use_container_width=True, key="gen_study"):
            with st.spinner("⏳ Generating..."):
                generate_study_callback()
    else:
        st.success("✅ Ready")
        st.markdown("### 📇 Flashcards")
        for i, card in enumerate(st.session_state.flashcards, 1):
            st.markdown(f"**Card {i}**")
            st.markdown(f'<div class="question-box">❓ {card["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="answer-box">✅ {card["answer"]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ❓ Quiz")
        for line in str(st.session_state.quiz).split('\n'):
            if line.strip():
                if any(line.strip().lower().startswith(p) for p in ['question', 'q1', 'q2', 'q3']):
                    st.markdown(f'<div class="quiz-question-container"><strong>{line.strip()}</strong></div>', unsafe_allow_html=True)
                elif any(line.strip().startswith(p) for p in ['A)', 'B)', 'C)', 'D)']):
                    st.markdown(f'<div class="quiz-option-item">{line.strip()}</div>', unsafe_allow_html=True)
                elif any(line.strip().lower().startswith(p) for p in ['answer', 'correct']):
                    st.markdown(f'<div class="quiz-answer">{line.strip()}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(line)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Regenerate", use_container_width=True, key="regen_study"):
                st.session_state.flashcards = None
                st.session_state.quiz = None
                st.rerun()
        with col2:
            st.download_button("📥 Export", export_callback(), f"study_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", "text/markdown", use_container_width=True, key="export_study")

def render_navigation_tab(generate_navigation_callback):
    """הצג טאב ניווט חכם"""
    st.title("🧭 Smart Navigation")
    if st.session_state.navigation is None:
        if st.button("Generate", use_container_width=True, key="gen_nav"):
            with st.spinner("⏳ Generating..."):
                generate_navigation_callback()
    else:
        st.success("✅ Article Structure")
        for item in st.session_state.navigation:
            st.markdown(f'<div class="nav-item"><div class="nav-item-title">📌 {item["title"]}</div><p><strong>Preview:</strong> {item["content_preview"]}</p><p><strong>Explanation:</strong> {item["explanation"]}</p></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("🔄 Regenerate", use_container_width=True, key="regen_nav"):
            st.session_state.navigation = None
            st.rerun()

def render_footer():
    """הצג footer"""
    st.markdown('<div class="footer"><p>🚀 AI Web Knowledge Summarizer</p></div>', unsafe_allow_html=True)

def generate_export_content():
    """יצור תוכן ל-export"""
    content = f"# AI Web Knowledge Summarizer\n\n"
    if st.session_state.documents and len(st.session_state.documents) > 0:
        page_title = st.session_state.documents[0].metadata.get('title', 'Unknown')
        content += f"# {page_title}\n\n"
    content += f"**URL:** {st.session_state.current_url}\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    if st.session_state.summaries:
        content += f"## Summaries\n\n### TL;DR\n{st.session_state.summaries['TLDR']}\n\n### Medium\n{st.session_state.summaries['Medium']}\n\n### Deep\n{st.session_state.summaries['Deep']}\n\n"
    if st.session_state.flashcards:
        content += "## Flashcards\n\n"
        for i, card in enumerate(st.session_state.flashcards, 1):
            content += f"### Card {i}\n**Q:** {card['question']}\n**A:** {card['answer']}\n\n"
    if st.session_state.quiz:
        content += f"## Quiz\n\n{st.session_state.quiz}"
    return content
