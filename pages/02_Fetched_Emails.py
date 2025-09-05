import streamlit as st

st.set_page_config(page_title="Fetched Emails", page_icon="📧")

st.title("📧 Your Fetched Emails")

if "fetched_emails" not in st.session_state or not st.session_state.fetched_emails:
    st.warning("No emails fetched yet. Go back to the main page and fetch emails first.")
else:
    for idx, mail in enumerate(st.session_state.fetched_emails, 1):
        with st.expander(f"Email {idx}: {mail['subject']}"):
            st.write(f"**From:** {mail['from']}")
            st.write(f"**Date:** {mail['date']}")
            st.write("---")
            st.write(mail['body'][:1000] + "..." if len(mail['body']) > 1000 else mail['body'])
