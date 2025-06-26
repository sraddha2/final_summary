import os
import streamlit as st
from dotenv import load_dotenv
from summarizer.azure_summarizer import AzureSummarizer
from utils.web_loader import load_web_content

# Custom page config
st.set_page_config(
    page_title="Azure Website/Text Summarizer",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .main { background-color: #f5f7fa; }
        .stButton>button {
            color: white;
            background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
            border-radius: 8px;
            font-size: 18px;
            padding: 0.5em 2em;
        }
        .stTextInput>div>div>input, .stTextArea>div>textarea {
            background-color: #eaf6fb;
            border-radius: 8px;
        }
        .summary-box {
            background-color: #e3fcec;
            border-radius: 8px;
            padding: 1em;
            margin-top: 1em;
            font-size: 1.1em;
            border: 1px solid #b2f2d7;
        }
        .footer {
            margin-top: 2em;
            color: #888;
            font-size: 0.9em;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv(dotenv_path=".env")

# Get key and endpoint from environment variables
text_analytics_key = os.environ.get("AZURE_TEXT_ANALYTICS_KEY")
text_analytics_endpoint = os.environ.get("AZURE_TEXT_ANALYTICS_ENDPOINT")

# Initialize summarizer with key and endpoint
summarizer = AzureSummarizer(
    key=text_analytics_key,
    endpoint=text_analytics_endpoint
)

st.markdown("<h1 style='text-align: center; color: #0072ff;'>Azure Website/Text Summarizer & Q&A</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Summarize or ask questions about any text or website content using Azure AI</p>", unsafe_allow_html=True)

mode = st.radio("Choose mode:", ("Summarization", "Q&A (RAG)"), horizontal=True)
option = st.radio("Choose input type:", ("📝 Text", "🌐 URL"), horizontal=True)

def display_summary(summary):
    st.markdown("<div class='summary-box'><b>Summary:</b><br>", unsafe_allow_html=True)
    sentences = [s.strip() for s in summary.replace('\n', ' ').split('. ') if s.strip()]
    for s in sentences:
        if not s.endswith('.'):
            s += '.'
        st.markdown(f"- {s}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if mode == "Summarization":
    summary_type = st.radio("Summary length:", ("Short (≈50 words)", "Long (≈100 words)"), horizontal=True)
    max_sentences = 3 if summary_type == "Short (≈50 words)" else 6

    if option == "📝 Text":
        user_text = st.text_area("Enter text to summarize:", height=200, placeholder="Paste or type your text here...")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            summarize_btn = st.button("✨ Summarize Text")
        if summarize_btn:
            if user_text.strip():
                with st.spinner("Summarizing..."):
                    try:
                        summary = summarizer.summarize_text(user_text, max_sentences=max_sentences)
                        display_summary(summary)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter some text to summarize.")
    else:
        url = st.text_input("Enter URL to summarize:", placeholder="https://example.com")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            summarize_btn = st.button("🌍 Summarize URL")
        if summarize_btn:
            if url.strip():
                with st.spinner("Loading and summarizing content..."):
                    try:
                        summary = summarizer.summarize_url(url, max_sentences=max_sentences)
                        display_summary(summary)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter a URL to summarize.")

else:  # Q&A (RAG)
    if option == "📝 Text":
        user_text = st.text_area("Enter context text for Q&A:", height=200, placeholder="Paste or type your text here...")
        question = st.text_input("Ask a question about the above text:")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            qa_btn = st.button("🔎 Get Answer")
        if qa_btn:
            if user_text.strip() and question.strip():
                with st.spinner("Searching for answer..."):
                    try:
                        answer = summarizer.answer_question(user_text, question)
                        st.markdown(f"<div class='summary-box'><b>Answer:</b><br>{answer}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter both context and a question.")
    else:
        url = st.text_input("Enter URL for Q&A:", placeholder="https://example.com")
        question = st.text_input("Ask a question about the website content:")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            qa_btn = st.button("🔎 Get Answer from URL")
        if qa_btn:
            if url.strip() and question.strip():
                with st.spinner("Loading content and searching for answer..."):
                    try:
                        content = load_web_content(url)
                        answer = summarizer.answer_question(content, question)
                        st.markdown(f"<div class='summary-box'><b>Answer:</b><br>{answer}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter both a URL and a question.")

st.markdown(
    "<div class='footer'>Made with ❤️ using Azure AI & Streamlit | <a href='https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/' target='_blank'>Learn more</a></div>",
    unsafe_allow_html=True
)
