
# import streamlit as st
# import numpy as np 
# import imaplib, email

# from src.data_ingestion.document_parser import parse_txt, parse_pdf
# from src.data_ingestion.web_scraper import fetch_and_clean_url
# from src.processing.semantic_search import find_relevant_documents
# from src.processing.chatbot import analyze_text_with_gemini, get_gemini_response, generate_meeting_briefing
# from src.processing.visualizer import generate_word_cloud


# def local_summarize(text: str, max_sentences: int = 3) -> str:
#     """Simple local summarizer (extracts first N sentences)."""
#     sentences = text.split(". ")
#     return ". ".join(sentences[:max_sentences]) + ("..." if len(sentences) > max_sentences else "")


# st.set_page_config(page_title="Intelligent Productivity Assistant", page_icon="🧠", layout="wide")

# CUSTOM_CSS = """
# body { background-color: #F0F2F5; font-family: 'Segoe UI', 'Roboto', sans-serif; }
# .card { background-color: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; 
#         box-shadow: 0 4px 12px rgba(0,0,0,0.08); color: #333; }
# .st-emotion-cache-16txtl3 { background: linear-gradient(180deg, #FFFFFF, #F0F2F5); 
#         border-right: 1px solid #DDD; }
# .stButton>button { border-radius: 20px; border: 1px solid #2B80FF; background-color: #2B80FF; 
#         color: white; padding: 10px 24px; font-weight: bold; transition: all 0.3s ease; 
#         box-shadow: 0 4px 12px rgba(43, 128, 255, 0.3); }
# .stButton>button:hover { background-color: #0060E0; border-color: #0060E0; transform: translateY(-2px); 
#         box-shadow: 0 6px 16px rgba(43, 128, 255, 0.4); }
# """
# st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)


# # ---------------- SESSION STATE ----------------
# if 'results' not in st.session_state:
#     st.session_state.results = None
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'analyzed_sources' not in st.session_state:
#     st.session_state.analyzed_sources = {}
# if 'meeting_notes' not in st.session_state:
#     st.session_state.meeting_notes = {}
# if 'mock_mode' not in st.session_state:
#     st.session_state.mock_mode = False
# if 'summarizer_choice' not in st.session_state:
#     st.session_state.summarizer_choice = "Gemini AI"


# # ---------------- SIDEBAR ----------------
# with st.sidebar:
#     st.header("⚙️ Settings")
#     st.session_state.mock_mode = st.checkbox("Enable Mock Mode", value=st.session_state.mock_mode)
#     st.session_state.summarizer_choice = st.radio(
#         "Summarizer",
#         ["Gemini AI", "Local Summarizer"],
#         index=0 if st.session_state.summarizer_choice == "Gemini AI" else 1
#     )

#     st.markdown("---")
#     st.header("📂 Analyze a Source")
#     uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])
#     url_input = st.text_input("...or enter a URL:")
#     analyze_url_button = st.button("Analyze Source", use_container_width=True)

#     st.markdown("---")
#     st.header("📅 Meeting Prep Assistant")
#     meeting_topic = st.text_input("Meeting Topic")
#     prep_button = st.button("Generate Briefing", use_container_width=True)

#     st.markdown("---")
#     st.header("📧 Email Analysis")
#     user_email = st.text_input("Enter your email (Gmail/Outlook):")
#     app_password = st.text_input("Enter your app password", type="password")
#     fetch_emails_button = st.button("Fetch Emails", use_container_width=True)


# # ---------------- CORE FUNCTIONS ----------------
# def run_analysis(source_text, source_name):
#     """Analyze text with selected summarizer."""
#     with st.spinner(f"Analyzing {source_name}..."):
#         if st.session_state.mock_mode:
#             analysis_report = f"[MOCK SUMMARY for {source_name}] {source_text[:150]}..."
#         elif st.session_state.summarizer_choice == "Local Summarizer":
#             analysis_report = local_summarize(source_text)
#         else:
#             analysis_report = analyze_text_with_gemini(source_text)

#         st.session_state.analyzed_sources[source_name] = {
#             "report": analysis_report,
#             "full_text": source_text,
#             "type": "document" if source_name.endswith(('.txt', '.pdf')) else "link"
#         }
#         st.session_state.results = {"report": analysis_report, "source_name": source_name}
#         st.success("Analysis complete!")


# def run_meeting_prep(topic):
#     """Generate meeting briefing note."""
#     with st.spinner("Preparing meeting note..."):
#         relevant_docs = find_relevant_documents(
#             topic, {k: v["full_text"] for k, v in st.session_state.analyzed_sources.items()}
#         )
#         if st.session_state.mock_mode:
#             briefing = f"[MOCK MEETING NOTE for {topic}] Key points..."
#         else:
#             briefing = generate_meeting_briefing(topic, relevant_docs)

#         st.session_state.meeting_notes[topic] = briefing
#         st.session_state.results = {"report": briefing, "source_name": f"Meeting: {topic}"}
#         st.success("Briefing note ready!")


# def fetch_emails(user_email, app_password):
#     """Fetch last 5 emails from Gmail/Outlook."""
#     try:
#         # Detect provider
#         if any(domain in user_email for domain in ["outlook.com", "hotmail.com", "live.com"]):
#             server = "outlook.office365.com"
#         elif any(domain in user_email for domain in ["gmail.com", "googlemail.com"]):
#             server = "imap.gmail.com"
#         else:
#             st.error("Unsupported email provider. Please use Gmail or Outlook/Hotmail.")
#             return

#         # Connect IMAP
#         mail = imaplib.IMAP4_SSL(server)
#         mail.login(user_email, app_password)
#         mail.select("inbox")

#         # Get latest 5 emails
#         result, data = mail.search(None, "ALL")
#         mail_ids = data[0].split()
#         latest_ids = mail_ids[-5:]

#         for i in latest_ids:
#             result, msg_data = mail.fetch(i, "(RFC822)")
#             raw_msg = msg_data[0][1]
#             msg = email.message_from_bytes(raw_msg)

#             subject = msg["subject"] or "(No Subject)"
#             from_ = msg["from"] or "(Unknown sender)"

#             # Extract plain text body
#             body = ""
#             if msg.is_multipart():
#                 for part in msg.walk():
#                     if part.get_content_type() == "text/plain":
#                         body = part.get_payload(decode=True).decode(errors="ignore")
#                         break
#             else:
#                 body = msg.get_payload(decode=True).decode(errors="ignore")

#             run_analysis(body, f"Email: {subject} (from {from_})")

#         st.success("✅ Emails analyzed successfully!")

#     except Exception as e:
#         st.error(f"Email fetch error: {e}")


# # ---------------- APP LOGIC ----------------
# if uploaded_file:
#     doc_text = parse_txt(uploaded_file) if uploaded_file.type == "text/plain" else parse_pdf(uploaded_file)
#     if doc_text and "Error:" not in doc_text:
#         run_analysis(doc_text, uploaded_file.name)
#     else:
#         st.error(doc_text or "Could not read text from file.")

# if analyze_url_button:
#     if url_input:
#         web_text = fetch_and_clean_url(url_input)
#         if "Error:" not in web_text:
#             run_analysis(web_text, url_input)
#         else:
#             st.error(web_text)
#     else:
#         st.warning("Please enter a URL.")

# if prep_button:
#     if meeting_topic:
#         run_meeting_prep(meeting_topic)
#     else:
#         st.warning("Please enter a meeting topic.")

# if fetch_emails_button:
#     if user_email and app_password:
#         fetch_emails(user_email, app_password)
#     else:
#         st.warning("Please enter both email and app password.")


# # ---------------- MAIN PAGE ----------------
# st.title("🧠 Intelligent Productivity Assistant")

# st.subheader("📜 Analysis & Meeting History")

# if st.session_state.analyzed_sources or st.session_state.meeting_notes:
#     all_entries = {
#         **st.session_state.analyzed_sources,
#         **{f"Meeting: {k}": {"report": v, "full_text": v, "type": "meeting"} 
#            for k, v in st.session_state.meeting_notes.items()}
#     }

#     for name, data in all_entries.items():
#         with st.expander(name, expanded=(st.session_state.results and st.session_state.results["source_name"] == name)):
#             st.markdown(data["report"])

#             if data.get("type") in ["document", "link", "email"]:
#                 st.markdown("---")
#                 wordcloud_figure = generate_word_cloud(data.get('full_text', ""))
#                 if wordcloud_figure:
#                     st.pyplot(wordcloud_figure, use_container_width=True)
#                 else:
#                     st.info("A meaningful visualization could not be generated for this source.")

#             if st.button("❌ Delete", key=f"delete_{name}"):
#                 if data["type"] == "meeting":
#                     del st.session_state.meeting_notes[name.replace("Meeting: ", "")]
#                 else:
#                     del st.session_state.analyzed_sources[name]
#                 st.rerun()
# else:
#     st.info("No analyses or meeting notes yet. Upload a document, enter a URL, fetch emails, or create a meeting note.")


# # ---------------- CHATBOT ----------------
# st.markdown("---")
# st.subheader("💬 Chat with all content")

# for author, message in st.session_state.chat_history:
#     with st.chat_message(author):
#         st.markdown(message)

# user_question = st.chat_input("Ask a question (about any analyzed content or meeting note)...")
# if user_question:
#     st.session_state.chat_history.append(("user", user_question))
#     with st.chat_message("user"):
#         st.markdown(user_question)

#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             combined_text = "\n".join(
#                 [v["full_text"] for v in st.session_state.analyzed_sources.values()]
#                 + list(st.session_state.meeting_notes.values())
#             )
#             if st.session_state.mock_mode:
#                 response = f"[MOCK RESPONSE] {user_question}"
#             else:
#                 response = get_gemini_response(combined_text, user_question)
#             st.markdown(response)
#             st.session_state.chat_history.append(("assistant", response))













# app.py
import os
import time
import smtplib
from email.message import EmailMessage

import streamlit as st

# --- Project helpers (make sure these exist in your src/ package) ---
from src.data_ingestion.document_parser import parse_txt, parse_pdf
from src.data_ingestion.web_scraper import fetch_and_clean_url
from src.data_ingestion.gmail_reader import fetch_emails_imap
from src.processing.semantic_search import find_relevant_documents
from src.processing.chatbot import (
    analyze_text_with_gemini,
    get_gemini_response,
    generate_meeting_briefing,
)
from src.processing.visualizer import generate_word_cloud


# ---------------------------
# Utility / local functions
# ---------------------------
def local_summarize(text: str, max_sentences: int = 3) -> str:
    """Very small local extractor: first N sentences (fallback / fast)."""
    sentences = [s.strip() for s in text.replace("\n", " ").split(". ") if s.strip()]
    if not sentences:
        return ""
    snippet = ". ".join(sentences[:max_sentences])
    return snippet + ("..." if len(sentences) > max_sentences else "")


def send_email_smtp(user_email: str, user_password: str, to_addr: str, subject: str, body: str):
    """Send a simple email via Gmail SMTP (uses SSL)."""
    try:
        msg = EmailMessage()
        msg["From"] = user_email
        msg["To"] = to_addr
        msg["Subject"] = subject
        msg.set_content(body)

        # Gmail SSL port 465
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(user_email, user_password)
            smtp.send_message(msg)
        return True, "Email sent successfully."
    except Exception as e:
        return False, f"Failed to send email: {e}"


def run_analysis(source_text: str, source_name: str, source_type: str = "document"):
    """
    Run analysis according to user's summarizer choice or mock mode.
    Stores results in st.session_state.analyzed_sources.
    """
    if not source_text:
        return

    with st.spinner(f"Analyzing '{source_name}'..."):
        if st.session_state.mock_mode:
            report = f"[MOCK] Summary for {source_name}: {source_text[:200]}..."
        elif st.session_state.summarizer_choice == "Local Summarizer":
            report = local_summarize(source_text, max_sentences=4)
        else:
            # Gemini (or similar) - can be slow; use spinner
            report = analyze_text_with_gemini(source_text)

    st.session_state.analyzed_sources[source_name] = {
        "report": report,
        "full_text": source_text,
        "type": source_type,
        "created_at": time.time(),
    }
    # keep the 'results' pointer for UI open state
    st.session_state.results = {"source_name": source_name, "report": report}
    st.success(f"Analysis stored: {source_name}")


def run_meeting_prep(topic: str):
    """Create meeting briefing using semantic search to find relevant docs."""
    with st.spinner("Finding relevant documents..."):
        sources_map = {k: v["full_text"] for k, v in st.session_state.analyzed_sources.items()}
        relevant_docs = find_relevant_documents(topic, sources_map)
    with st.spinner("Generating briefing..."):
        if st.session_state.mock_mode:
            briefing = f"[MOCK] Briefing for '{topic}': key points extracted..."
        else:
            briefing = generate_meeting_briefing(topic, relevant_docs)
    st.session_state.meeting_notes[topic] = briefing
    st.session_state.results = {"source_name": f"Meeting: {topic}", "report": briefing}
    st.success(f"Meeting briefing ready: {topic}")


# ---------------------------
# Page config & CSS
# ---------------------------
st.set_page_config(page_title="Intelligent Productivity Assistant", page_icon="🧠", layout="wide")

CUSTOM_CSS = """
/* Minimal styling tweaks */
body { background-color: #0f1720; color: #fff; }
.stApp { color: #fff; }
"""
st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)


# ---------------------------
# Session-state initialization
# ---------------------------
if "analyzed_sources" not in st.session_state:
    st.session_state.analyzed_sources = {}  # name -> {report, full_text, type}
if "meeting_notes" not in st.session_state:
    st.session_state.meeting_notes = {}
if "fetched_emails" not in st.session_state:
    st.session_state.fetched_emails = []  # temporary inbox preview
if "results" not in st.session_state:
    st.session_state.results = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mock_mode" not in st.session_state:
    st.session_state.mock_mode = False
if "summarizer_choice" not in st.session_state:
    st.session_state.summarizer_choice = "Gemini AI"
if "auto_analyze" not in st.session_state:
    st.session_state.auto_analyze = True


# ---------------------------
# Sidebar (controls)
# ---------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.mock_mode = st.checkbox("Enable Mock Mode", value=st.session_state.mock_mode)
    st.session_state.summarizer_choice = st.radio(
        "Summarizer",
        ["Gemini AI", "Local Summarizer"],
        index=0 if st.session_state.summarizer_choice == "Gemini AI" else 1,
    )
    st.session_state.auto_analyze = st.checkbox(
        "Auto-analyze on upload/fetch", value=st.session_state.auto_analyze
    )
    st.markdown("---")

    # Gmail inputs (Option 2)
    st.header("📧 Gmail (IMAP / SMTP)")
    gmail_user = st.text_input("Gmail address", value="", placeholder="you@gmail.com", key="gmail_user")
    gmail_pass = st.text_input("App password", value="", type="password", key="gmail_pass")
    gmail_folder = st.text_input("Folder (IMAP)", value="INBOX", key="gmail_folder")
    gmail_count = st.number_input("Emails to fetch", min_value=1, max_value=20, value=5, key="gmail_count")
    fetch_gmail_btn = st.button("Fetch emails", key="fetch_gmail_btn", use_container_width=True)
    st.markdown("Fetches headers/snippets. Click 'Analyze' for full parsing & attachment processing.")


    emails = st.session_state.get("fetched_emails", [])
    if emails:
     st.subheader("📧 Fetched Emails")
     for i, mail in enumerate(emails, start=1):
        with st.expander(f"{i}. {mail['subject']}"):
            st.markdown(f"**From:** {mail['from']}")
            st.markdown(f"**Date:** {mail['date']}")
            st.markdown("---")
            st.write(mail["body"][:1000])  # show preview of body
            if mail["attachments"]:
                st.markdown("**Attachments:**")
                for att in mail["attachments"]:
                    st.text(f"- {att['filename']}")




    with st.expander("✉️ Compose / Send Email (uses SMTP)"):
        send_to = st.text_input("To (email address)", key="compose_to")
        send_subject = st.text_input("Subject", key="compose_subject")
        send_body = st.text_area("Body", key="compose_body", height=160)
        send_btn = st.button("Send Email", key="send_email_btn", use_container_width=True)

    st.markdown("---")
    st.header("📁 Input")
    uploaded_files = st.file_uploader("Upload .pdf or .txt (multiple allowed)", type=["pdf", "txt"], accept_multiple_files=True)
    st.markdown("---")
    st.markdown("Choose whether to auto-analyze uploaded files or fetch results and analyze individually.")



# ---------------------------
# Handle Compose / Send
# ---------------------------
if "send_email_btn" in locals() and send_btn:
    if not gmail_user or not gmail_pass:
        st.sidebar.error("Enter Gmail address and App password in the Gmail section above to send email.")
    elif not send_to:
        st.sidebar.error("Enter recipient email address.")
    else:
        ok, msg = send_email_smtp(gmail_user, gmail_pass, send_to, send_subject or "(no subject)", send_body or "")
        if ok:
            st.sidebar.success(msg)
        else:
            st.sidebar.error(msg)


# ---------------------------
# Process uploaded files (store parsed text; analyze if auto_analyze True)
# ---------------------------
if uploaded_files:
    for up in uploaded_files:
        key_name = up.name
        # If not already parsed/stored, parse and either analyze immediately or store pending
        if key_name not in st.session_state.analyzed_sources:
            try:
                if up.type == "text/plain" or key_name.lower().endswith(".txt"):
                    text = parse_txt(up)
                else:
                    text = parse_pdf(up)
            except Exception as e:
                text = f"Error: Could not parse uploaded file: {e}"

            if isinstance(text, str) and not text.startswith("Error:"):
                if st.session_state.auto_analyze:
                    run_analysis(text, key_name, source_type="document")
                else:
                    # store as a pending entry with empty report (user can click analyze later)
                    st.session_state.analyzed_sources[key_name] = {
                        "report": None,
                        "full_text": text,
                        "type": "document",
                        "created_at": time.time(),
                    }
                    st.success(f"Parsed (pending): {key_name}")
            else:
                st.error(text)


# ---------------------------
# Fetch Gmail (headers/snippet) - store in fetched_emails for preview
# ---------------------------
if fetch_gmail_btn:
    if not gmail_user or not gmail_pass:
        st.sidebar.error("Enter Gmail address and App password above to fetch emails.")
    else:
        try:
            fetched = fetch_emails_imap(
                user_email=gmail_user,
                user_password=gmail_pass,
                count=int(gmail_count),
                folder=gmail_folder
            )
            st.session_state.fetched_emails = fetched or []
            if fetched:
                st.sidebar.success(f"Fetched {len(fetched)} emails (preview).")
            else:
                st.sidebar.warning("No emails fetched. Please check folder, credentials, or IMAP access.")
        except Exception as e:
            st.sidebar.error(f"Failed to fetch emails: {e}")



# ---------------------------
# URLs: analyze on demand
# ---------------------------
st.markdown("---")
st.header("🔗 Analyze a URL")
url_input = st.text_input("Enter a URL to analyze", key="url_input")
analyze_url_btn = st.button("Analyze URL", key="analyze_url_btn")
if analyze_url_btn:
    if not url_input:
        st.warning("Enter a URL first.")
    else:
        web_text = fetch_and_clean_url(url_input)
        if isinstance(web_text, str) and web_text.startswith("Error:"):
            st.error(web_text)
        else:
            if st.session_state.auto_analyze:
                run_analysis(web_text, url_input, source_type="link")
            else:
                st.session_state.analyzed_sources[url_input] = {
                    "report": None,
                    "full_text": web_text,
                    "type": "link",
                    "created_at": time.time(),
                }
                st.success("URL fetched (pending analysis).")


# ---------------------------
# Meeting prep (sidebar button)
# ---------------------------
if "prep_button" not in locals():
    # If not defined earlier, create dummy so access is safe.
    pass

if "Generate Briefing" in st.session_state:
    pass

# We'll handle meeting generation with the sidebar button variable name above:
if "prep_button" in locals() and False:
    # placeholder - code should never reach, left intentionally
    pass

# In current layout meeting_topic and button are in sidebar - get them by key lookup:
meeting_topic = st.session_state.get("sidebar_meeting_topic", None)
# But earlier we didn't store meeting_topic under a key; we'll just add a small meeting section in main UI below.


# ---------------------------
# Main UI: Title & History
# ---------------------------
st.title("🧠 Intelligent Productivity Assistant")
st.subheader("📜 Analysis & Meeting History")

# Combined entries: analyzed_sources and meeting_notes
def get_all_entries():
    entries = {}
    # preserve insertion order via created_at (if present)
    # analyzed_sources
    for k, v in st.session_state.analyzed_sources.items():
        entries[k] = v.copy()
    # meeting notes (prefix key)
    for topic, note in st.session_state.meeting_notes.items():
        entries[f"Meeting: {topic}"] = {"report": note, "full_text": note, "type": "meeting"}
    return entries


all_entries = get_all_entries()

if not all_entries:
    st.info("No analyzed content yet. Upload files, analyze a URL, or fetch & analyze Gmail emails.")
else:
    # Show fetched emails preview (if any) and allow analyzing them
    if st.session_state.fetched_emails:
        st.markdown("### ✉️ Fetched Gmail (preview)")
        for idx, em in enumerate(st.session_state.fetched_emails):
            subject = em.get("subject", "(no subject)")
            frm = em.get("from", "")
            date = em.get("date", "")
            with st.expander(f"{subject} — {frm} — {date}", expanded=False):
                snippet = (em.get("body") or "")[:1000]
                st.markdown(snippet + ("..." if len(snippet) > 1000 else ""))
                # Analyze body button
                if st.button(f"Analyze email body #{idx}", key=f"analyze_email_body_{idx}"):
                    run_analysis(em.get("body", ""), f"Email: {subject}", source_type="email")
                # attachments
                attachments = em.get("attachments", []) or []
                for a_i, att in enumerate(attachments):
                    st.markdown(f"- Attachment: **{att.get('filename')}**")
                    if st.button(f"Analyze attachment {a_i} of email {idx}", key=f"analyze_att_{idx}_{a_i}"):
                        # att['content'] expected to be text already after parse in gmail_reader
                        run_analysis(att.get("content", ""), f"{subject} - Attachment: {att.get('filename')}", source_type="attachment")

    st.markdown("---")
    # Show all analyzed + meeting entries in expanders
    for name in list(all_entries.keys()):
        data = all_entries[name]
        expanded_default = st.session_state.results and st.session_state.results.get("source_name") == name
        with st.expander(name, expanded=expanded_default):
            report = data.get("report") or "(No summary generated yet. Click 'Analyze' to generate.)"
            full_text = data.get("full_text", "")
            st.markdown("**Summary / Report:**")
            st.markdown(report)

            # Show download button for report + full text
            col_a, col_b = st.columns([1, 1])
            with col_a:
                # Download the report (if exists)
                if report:
                    st.download_button(
                        f"📥 Download Report ({name})",
                        data=report,
                        file_name=f"{name.replace(' ', '_')}_report.txt",
                        mime="text/plain",
                        key=f"dl_report_{name}",
                    )
            # with col_b:
            #     if full_text:
            #         st.download_button(
            #             f"📥 Download Source ({name})",
            #             data=full_text,
            #             file_name=f"{name.replace(' ', '_')}_fulltext.txt",
            #             mime="text/plain",
            #             key=f"dl_full_{name}",
            #         )

            # Visualize (word cloud) only for document/link/email/attachment
            if data.get("type") in ("document", "link", "email", "attachment"):
                st.markdown("---")
                st.markdown("**Visualization (keywords)**")
                try:
                    fig = generate_word_cloud(full_text or "")
                    if fig:
                        st.pyplot(fig, use_container_width=True)
                    else:
                        st.info("Not enough content or no meaningful keywords to visualize.")
                except Exception as e:
                    st.error(f"Visualization error: {e}")

            # Provide Analyze button if report is None or if user wants to re-run
            if data.get("report") is None:
                if st.button(f"Analyze now ({name})", key=f"analyze_now_{name}"):
                    run_analysis(full_text, name, source_type=data.get("type", "document"))
            else:
                if st.button(f"Re-run analysis ({name})", key=f"re_analyze_{name}"):
                    run_analysis(full_text, name, source_type=data.get("type", "document"))

            # Delete button
            if st.button("❌ Delete this entry", key=f"delete_{name}"):
                # handle meeting vs normal
                if name.startswith("Meeting: "):
                    topic = name.replace("Meeting: ", "")
                    st.session_state.meeting_notes.pop(topic, None)
                else:
                    st.session_state.analyzed_sources.pop(name, None)
                st.success(f"Deleted: {name}")
                # Buttons cause rerun automatically; just continue to next entry.
                st.experimental_rerun() if hasattr(st, "experimental_rerun") else None


# ---------------------------
# Meeting Prep in main area (small UI)
# ---------------------------
st.markdown("---")
st.header("📅 Meeting Prep Assistant")
meeting_topic_main = st.text_input("What is your meeting about?", key="meeting_topic_main")
if st.button("Generate Briefing", key="generate_briefing_main"):
    if not meeting_topic_main:
        st.warning("Enter a meeting topic.")
    else:
        run_meeting_prep(meeting_topic_main)


# ---------------------------
# Chat assistant (unified across all content)
# ---------------------------
# st.markdown("---")
# st.header("💬 Chat with all content")

# # show previous chat
# if st.session_state.chat_history:
#     for i, (who, text) in enumerate(st.session_state.chat_history):
#         if who == "user":
#             st.markdown(f"**You:** {text}")
#         else:
#             st.markdown(f"**Assistant:** {text}")

# user_question = st.text_input("Ask a question about any analyzed content or meeting note...", key="chat_input")
# if st.button("Send", key="chat_send"):
#     if not user_question:
#         st.warning("Write a question first.")
#     else:
#         # Build combined context from all analyzed sources + meeting notes
#         combined_texts = [v.get("full_text", "") for v in st.session_state.analyzed_sources.values() if v.get("full_text")]
#         combined_texts += [v for v in st.session_state.meeting_notes.values()]
#         combined_context = "\n\n".join(combined_texts)

#         st.session_state.chat_history.append(("user", user_question))
#         with st.spinner("Thinking..."):
#             if st.session_state.mock_mode:
#                 reply = f"[MOCK] I would answer: {user_question}"
#             else:
#                 # Call the external LLM-based function
#                 reply = get_gemini_response(combined_context, user_question)
#         st.session_state.chat_history.append(("assistant", reply))
#         # Rerender (button click triggers rerun; we simply allow rerun to happen)





st.markdown("---")
st.subheader("💬 Chat with all content")

for author, message in st.session_state.chat_history:
    with st.chat_message(author):
        st.markdown(message)

user_question = st.chat_input("Ask a question (about any analyzed content or meeting note)...")
if user_question:
    st.session_state.chat_history.append(("user", user_question))
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            combined_text = "\n".join(
                [v["full_text"] for v in st.session_state.analyzed_sources.values()]
                + list(st.session_state.meeting_notes.values())
            )
            if st.session_state.mock_mode:
                response = f"[MOCK RESPONSE] {user_question}"
            else:
                response = get_gemini_response(combined_text, user_question)
            st.markdown(response)
            st.session_state.chat_history.append(("assistant", response))



# ---------------------------
# Final note
# ---------------------------
st.markdown("---")
st.caption("Tip: Use the 'Auto-analyze' toggle if you prefer immediate analysis on upload/fetch. "
           "If you run slow on Gemini, switch to 'Local Summarizer' for quick previews.")
