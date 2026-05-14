# 🚀 AI Web Knowledge Summarizer - RAG System


An advanced RAG (Retrieval-Augmented Generation) system that transforms any website into an interactive, searchable knowledge base. Powered by **LlamaIndex** and **Google Gemini**, this tool provides multi-level summarization, intelligent navigation, and automated study materials.

---

## 🎯 Project Overview
The **AI Web Knowledge Summarizer** allows users to input any URL (Wikipedia, blogs, research papers) and interact with the content in real-time. Instead of reading through pages of text, users can get instant summaries or ask specific questions backed by source-referenced data.

## 🧠 Core Functionality
1. **Smart Extraction**: Cleanly scrapes main content while removing ads, footers, and noise using `BeautifulSoup` and `LlamaIndex WebReader`.
2. **Semantic Indexing**: Processes text into chunks (300-500 words) and builds a `Vector Store Index` for precise retrieval.
3. **RAG Engine**: Executes real-time queries against the website’s content using Google Gemini API.

## 🔥 Key Features

### 📌 1. Tiered Smart Summarization
Get the information you need at the depth you want:
*   🟢 **TL;DR**: The "bottom line" in one single sentence.
*   🟡 **Medium**: A concise paragraph covering the core concepts.
*   🔴 **Deep**: A structured, section-by-section breakdown.

### 🔍 2. Interactive RAG Chat
Ask anything about the page:
*   *"Explain the difference between X and Y"*
*   *"What are the main requirements mentioned?"*
*   The system provides direct answers with references to specific parts of the page.

### 🧭 3. Smart Navigation
A semantic "Table of Contents" that extracts:
*   Original headers from the page.
*   Relevant context and summaries for each section.

### 🧪 4. Study Mode
Automatically transforms any article into learning materials:
*   **Flashcards**: Core terms and definitions.
*   **Quizzes**: Generated questions to test your knowledge.
*   **Summarized Notes**: Essential takeaways for quick review.

---

## 📦 System Architecture



1.  **Input**: User provides a URL.
2.  **Load & Clean**: Scrapes text and preserves metadata (headers, positions).
3.  **Chunking**: Splits data into semantic segments.
4.  **Indexing**: Generates embeddings and stores them in a Vector Index.
5.  **Querying**: Matches user questions to the most relevant chunks and generates a response via Gemini.

---

## 🛠️ Tech Stack
*   **Language**: Python 3.9+
*   **Framework**: [LlamaIndex](https://www.llamaindex.ai/) (Data Framework for LLMs)
*   **LLM**: [Google Gemini API](https://ai.google.dev/)
*   **Web Scraping**: BeautifulSoup4 / WebReader
*   **UI**: Streamlit (Optional / Recommended)

## 🚀 Quick Start

### 1. Installation
```bash
git clone [https://github.com/your-username/ai-web-knowledge-summarizer.git](https://github.com/your-username/ai-web-knowledge-summarizer.git)
cd ai-web-knowledge-summarizer
pip install -r requirements.txt
