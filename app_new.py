import streamlit as st
import logging
from config import setup_settings
from web_scraper import load_web_data
from index_builder import build_index
from features import generate_tiered_summary, smart_navigation, generate_study_material, answer_question
from ui import (
    setup_page, initialize_session_state, render_header, render_url_input,
    render_welcome, render_summary_tab, render_chat_tab, render_study_tab,
    render_navigation_tab, render_footer, generate_export_content
)

logger = logging.getLogger(__name__)

def main():
    # הגדרות
    setup_page()
    initialize_session_state()
    
    # אתחול מודלים
    try:
        llm, embed_model, provider = setup_settings()
    except RuntimeError as e:
        st.error(str(e))
        st.stop()
    
    # כותרת
    render_header(provider)
    
    # קלט URL
    url_input, analyze_button = render_url_input()
    
    # עיבוד URL
    if analyze_button and url_input:
        if not url_input.startswith(('http://', 'https://')):
            st.error("❌ Invalid URL")
        else:
            with st.spinner("📥 Loading..."):
                docs = load_web_data(url_input)
                if docs:
                    st.session_state.documents = docs
                    st.session_state.current_url = url_input
                    with st.spinner("🔨 Building index..."):
                        idx = build_index(docs)
                        if idx:
                            st.session_state.index = idx
                            st.session_state.chat_history = []
                            st.session_state.summaries = None
                            st.session_state.flashcards = None
                            st.session_state.quiz = None
                            st.session_state.navigation = None
                            st.success("✅ Done!")
                            st.rerun()
    
    # תוכן ראשי
    if st.session_state.index is None:
        render_welcome()
    else:
        st.markdown(f'<div class="status-badge status-success">✅ {st.session_state.current_url}</div>', unsafe_allow_html=True)
        
        # הצג כותרת המאמר
        if st.session_state.documents and len(st.session_state.documents) > 0:
            page_title = st.session_state.documents[0].metadata.get('title', 'Unknown')
            st.markdown(f'<h1 style="text-align: center; color: #667eea; margin: 1.5rem 0;">{page_title}</h1>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # טאבים
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "💬 Chat", "📚 Study", "🧭 Navigation"])
        
        with tab1:
            def generate_summary():
                s = generate_tiered_summary(st.session_state.index)
                if s:
                    st.session_state.summaries = s
                st.rerun()
            
            render_summary_tab(generate_summary, generate_export_content)
        
        with tab2:
            render_chat_tab(
                lambda q: answer_question(st.session_state.index, q)
            )
        
        with tab3:
            def generate_study():
                m = generate_study_material(st.session_state.index)
                if m:
                    st.session_state.flashcards = m["flashcards"]
                    st.session_state.quiz = m["quiz"]
                st.rerun()
            
            render_study_tab(generate_study, generate_export_content)
        
        with tab4:
            def generate_nav():
                nav = smart_navigation(st.session_state.index, st.session_state.documents)
                if nav:
                    st.session_state.navigation = nav
                st.rerun()
            
            render_navigation_tab(generate_nav)
    
    # Footer
    render_footer()

if __name__ == "__main__":
    main()
