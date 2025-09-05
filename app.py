# import streamlit as st

# # --- Import ALL Backend Modules ---
# from src.data_ingestion.document_parser import parse_txt, parse_pdf
# from src.data_ingestion.web_scraper import fetch_and_clean_url
# from src.processing.chatbot import analyze_text_with_gemini, get_gemini_response
# from src.processing.semantic_search import find_relevant_documents
# from src.processing.chatbot import generate_meeting_briefing

# # --- Page Configuration ---
# st.set_page_config(page_title="Intelligent Productivity Assistant", page_icon="🧠", layout="wide")

# # --- Custom CSS ---
# CUSTOM_CSS = """
# /* (Your existing CSS here) */
# body { background-color: #F0F2F5; font-family: 'Segoe UI', 'Roboto', sans-serif; }
# .card { background-color: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); color: #333; }
# .card-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 10px; color: #2B80FF; }
# /* ...and the rest of your CSS... */
# """
# st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)

# # --- App State Initialization ---
# if 'results' not in st.session_state:
#     st.session_state.results = None
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'current_source_id' not in st.session_state:
#     st.session_state.current_source_id = None

# # --- Sidebar UI ---
# with st.sidebar:
#     # This loads your new local logo file
#     # st.image("logo.png", width=100)
#     st.header("Analyze Document")
#     uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf"])
    
#     st.markdown("---")
#     st.header("Analyze a Web Page")
#     url_input = st.text_input("Enter a URL:")
#     analyze_url_button = st.button("Analyze URL", use_container_width=True)

#     st.markdown("---")
# st.header("Meeting Prep Assistant")
# meeting_topic = st.text_input("What is your meeting about?")
# prep_button = st.button("Generate Briefing", use_container_width=True)

#     # This loads your new local logo file


# # --- Main Page ---
# st.title("🧠 Intelligent Productivity Assistant")


# # --- Processing Logic ---
# def run_analysis(source_text, source_name):
#     with st.spinner(f"Gemini is analyzing your source..."):
#         # The new analysis is just one powerful function call
#         analysis_report = analyze_text_with_gemini(source_text)
        
#         # Store both the raw text (for the chatbot) and the formatted report
#         st.session_state.results = {'report': analysis_report, 'full_text': source_text, 'source_name': source_name}
#         st.session_state.current_source_id = source_name
#         st.success("Analysis complete!")

# # --- Trigger Analysis ---
# if uploaded_file and uploaded_file.name != st.session_state.current_source_id:
#     doc_text = parse_txt(uploaded_file) if uploaded_file.type == "text/plain" else parse_pdf(uploaded_file)
#     if doc_text:
#         run_analysis(doc_text, uploaded_file.name)

# if analyze_url_button:
#     if url_input and url_input != st.session_state.current_source_id:
#         web_text = fetch_and_clean_url(url_input)
#         if "Error:" not in web_text:
#             run_analysis(web_text, url_input)
#         else:
#             st.error(web_text)
#     elif not url_input:
#         st.warning("Please enter a URL.")




# # --- NEW: Meeting Prep Logic ---
# if prep_button:
#     if meeting_topic:
#         # Collect all analyzed texts from the session state
#         if 'analyzed_sources' not in st.session_state:
#             st.session_state.analyzed_sources = {}

#         # For this example, we'll assume the last analyzed text is available
#         if st.session_state.results:
#             full_text = st.session_state.results.get('full_text', "")
#             source_name = st.session_state.results.get('source_name', "Unknown")
#             st.session_state.analyzed_sources[source_name] = full_text

#         if not st.session_state.analyzed_sources:
#             st.warning("Please analyze at least one document or web page before preparing for a meeting.")
#         else:
#             with st.spinner("Finding relevant documents..."):
#                 relevant_docs = find_relevant_documents(meeting_topic, st.session_state.analyzed_sources)

#             with st.spinner("Gemini is preparing your briefing note..."):
#                 briefing_note = generate_meeting_briefing(meeting_topic, relevant_docs)

#                 # Display the briefing note
#                 st.header(f"📋 Briefing Note for: {meeting_topic}")
#                 st.markdown(briefing_note)
#                 # Clear old results to show the new briefing
#                 st.session_state.results = None 
#     else:
#         st.warning("Please enter a meeting topic.")



# # --- Display Results ---
# if st.session_state.results:
#     res = st.session_state.results
#     st.header(f"📬 Analysis of: {res['source_name']}")
    
#     # The display is now much simpler: just render the Markdown from Gemini
#     st.markdown(res['report'])
    
#     # --- Gemini Chatbot Interface ---
#     st.markdown("---")
#     st.header("💬 Chat with the Content")
    
#     if st.session_state.current_source_id != st.session_state.get('chat_source_id'):
#         st.session_state.chat_history = []
#         st.session_state.chat_source_id = st.session_state.current_source_id

#     for author, message in st.session_state.chat_history:
#         with st.chat_message(author):
#             st.markdown(message)
            
#     user_question = st.chat_input("Ask a question about the analyzed content...")
#     if user_question:
#         st.session_state.chat_history.append(("user", user_question))
#         with st.chat_message("user"):
#             st.markdown(user_question)
        
#         with st.chat_message("assistant"):
#             with st.spinner("Gemini is thinking..."):
#                 full_text = res.get('full_text', "")
#                 response = get_gemini_response(full_text, user_question)
#                 st.markdown(response)
#                 st.session_state.chat_history.append(("assistant", response))
# else:
#     st.info("Use the sidebar to analyze a document or a web page.")









import streamlit as st
import numpy as np # Add numpy import

# --- Import ALL Backend Modules ---
from src.data_ingestion.document_parser import parse_txt, parse_pdf
from src.data_ingestion.web_scraper import fetch_and_clean_url
from src.processing.semantic_search import find_relevant_documents
from src.processing.chatbot import analyze_text_with_gemini, get_gemini_response, generate_meeting_briefing

# --- Page Configuration ---
st.set_page_config(page_title="Intelligent Productivity Assistant", page_icon="🧠", layout="wide")

# --- Custom CSS ---
CUSTOM_CSS = """
/* (Your existing CSS here) */
body { background-color: #F0F2F5; font-family: 'Segoe UI', 'Roboto', sans-serif; }
.card { background-color: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); color: #333; }
.st-emotion-cache-16txtl3 { background: linear-gradient(180deg, #FFFFFF, #F0F2F5); border-right: 1px solid #DDD; }
.stButton>button { border-radius: 20px; border: 1px solid #2B80FF; background-color: #2B80FF; color: white; padding: 10px 24px; font-weight: bold; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(43, 128, 255, 0.3); }
.stButton>button:hover { background-color: #0060E0; border-color: #0060E0; transform: translateY(-2px); box-shadow: 0 6px 16px rgba(43, 128, 255, 0.4); }
"""
st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)

# --- App State Initialization ---
if 'results' not in st.session_state:
    st.session_state.results = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_source_id' not in st.session_state:
    st.session_state.current_source_id = None
if 'analyzed_sources' not in st.session_state:
    st.session_state.analyzed_sources = {}
if 'briefing_note' not in st.session_state:
    st.session_state.briefing_note = None

# --- Sidebar UI ---
with st.sidebar:
    st.header("Analyze a Source")
    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])
    
    st.markdown("---")
    url_input = st.text_input("...or enter a URL:")
    analyze_url_button = st.button("Analyze Source", use_container_width=True)
    
    # --- NEW: Meeting Prep now in the sidebar ---
    st.markdown("---")
    st.header("Meeting Prep Assistant")
    meeting_topic = st.text_input("What is your meeting about?")
    prep_button = st.button("Generate Briefing", use_container_width=True)

# --- Main Page ---
st.title("🧠 Intelligent Productivity Assistant")

# --- Processing Logic ---
def run_analysis(source_text, source_name):
    with st.spinner(f"Gemini is analyzing {source_name}..."):
        analysis_report = analyze_text_with_gemini(source_text)
        st.session_state.results = {'report': analysis_report, 'full_text': source_text, 'source_name': source_name}
        st.session_state.current_source_id = source_name
        st.session_state.analyzed_sources[source_name] = source_text # Store for meeting prep
        st.session_state.briefing_note = None # Clear old briefing
        st.success("Analysis complete!")

# --- Trigger Analysis ---
source_to_analyze = None
if uploaded_file and uploaded_file.name != st.session_state.current_source_id:
    doc_text = parse_txt(uploaded_file) if uploaded_file.type == "text/plain" else parse_pdf(uploaded_file)
    if doc_text and "Error:" not in doc_text:
        run_analysis(doc_text, uploaded_file.name)
    else:
        st.error(doc_text or "Could not read text from file.")

if analyze_url_button:
    if url_input and url_input != st.session_state.current_source_id:
        web_text = fetch_and_clean_url(url_input)
        if "Error:" not in web_text:
            run_analysis(web_text, url_input)
        else:
            st.error(web_text)
    elif not url_input:
        st.warning("Please enter a URL.")

# --- Trigger Meeting Prep ---
if prep_button:
    if meeting_topic and st.session_state.analyzed_sources:
        with st.spinner("Finding relevant documents..."):
            relevant_docs = find_relevant_documents(meeting_topic, st.session_state.analyzed_sources)
        with st.spinner("Gemini is preparing your briefing note..."):
            briefing = generate_meeting_briefing(meeting_topic, relevant_docs)
            st.session_state.briefing_note = briefing
            st.session_state.results = None # Clear old analysis to show briefing
    elif not st.session_state.analyzed_sources:
        st.warning("Please analyze at least one document or web page first.")
    else:
        st.warning("Please enter a meeting topic.")

# --- Display Results ---
if st.session_state.briefing_note:
    st.header(f"📋 Briefing Note for: {meeting_topic}")
    st.markdown(st.session_state.briefing_note)

elif st.session_state.results:
    res = st.session_state.results
    st.header(f"📬 Analysis of: {res['source_name']}")
    st.markdown(res['report'])
    
    # --- Gemini Chatbot Interface ---
    st.markdown("---")
    st.header("💬 Chat with the Content")
    
    if st.session_state.current_source_id != st.session_state.get('chat_source_id'):
        st.session_state.chat_history = []
        st.session_state.chat_source_id = st.session_state.current_source_id

    for author, message in st.session_state.chat_history:
        with st.chat_message(author):
            st.markdown(message)
            
    user_question = st.chat_input("Ask a question about the analyzed content...")
    if user_question:
        st.session_state.chat_history.append(("user", user_question))
        with st.chat_message("user"):
            st.markdown(user_question)
        
        with st.chat_message("assistant"):
            with st.spinner("Gemini is thinking..."):
                full_text = res.get('full_text', "")
                response = get_gemini_response(full_text, user_question)
                st.markdown(response)
                st.session_state.chat_history.append(("assistant", response))
else:
    st.info("Use the sidebar to analyze a document or a web page.")





