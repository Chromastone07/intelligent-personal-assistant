import os
import google.generativeai as genai
from googleapiclient.discovery import build
from dotenv import load_dotenv

# --- API Configuration ---
load_dotenv()
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=gemini_api_key)
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    
    # Define the search tool function that the model can call
    def search_web(query: str):
        """Performs a web search for the given query and returns top results as a string."""
        print(f"--- Performing web search for: {query} ---")
        try:
            service = build("customsearch", "v1", developerKey=google_api_key)
            res = service.cse().list(q=query, cx=search_engine_id, num=3).execute()
            snippets = [item.get('snippet', '') for item in res.get('items', [])]
            return "\n".join(snippets)
        except Exception as e:
            return f"Search failed: {e}"

    # Initialize the Gemini model
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    
except Exception as e:
    print(f"Error configuring APIs: {e}")
    model = None

# --- Main Functions ---

def analyze_text_with_gemini(document_text: str) -> str:
    # (This function is already correct and does not need changes)
    if not model: return "Error: Gemini API not configured."
    if not document_text or len(document_text.strip()) < 50:
        return "The source text is too short for a meaningful analysis."
    prompt = f"""
    You are an expert productivity assistant...
    ## 📝 AI Summary...
    ## 🎯 Extracted Tasks...
    ## 🗓️ Key Deadlines...
    DOCUMENT TEXT: --- {document_text} ---
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during Gemini analysis: {e}"

def get_gemini_response(document_text: str, user_question: str) -> str:
    """
    Answers a user's question, with the ability to use a web search tool.
    """
    if not model:
        return "Error: APIs are not configured. Check your API keys."
    if not user_question:
        return "Please ask a question."
        
    prompt = f"""
    You are a helpful assistant. Your primary goal is to answer the user's question based on the DOCUMENT TEXT provided.
    First, analyze the user's question and the document text.
    If the answer is fully contained within the document, answer using only that text.
    However, if the user asks for more details on a topic only mentioned briefly, or for information clearly outside the document, you MUST use the `search_web` tool to find the information online.
    Finally, formulate a comprehensive answer based on all available information.

    DOCUMENT TEXT:
    ---
    {document_text}
    ---

    USER QUESTION: {user_question}
    """
    
    try:
        # Use a more direct method for tool calling
        response = model.generate_content(
            prompt,
            tools=[search_web]
        )
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with the Gemini API: {e}"
    

# (Add this new function to your existing chatbot.py file)

def generate_meeting_briefing(meeting_topic: str, relevant_texts: list) -> str:
    """
    Uses Gemini to generate a briefing note for a meeting based on relevant texts.
    """
    if not model:
        return "Error: Gemini API not configured."
    if not relevant_texts:
        return "Could not find any relevant documents to generate a briefing."

    # Combine the relevant texts into a single context block
    context = "\n\n---\n\n".join(relevant_texts)
    
    prompt = f"""
    You are an expert productivity assistant. Your task is to generate a concise briefing note for an upcoming meeting.
    The meeting is about: "{meeting_topic}".

    Use the following CONTEXT DOCUMENTS to prepare the briefing. Your output should be structured with Markdown headings.

    1.  **Key Points Summary:** Summarize the most critical information from the documents that relates directly to the meeting topic.
    2.  **Relevant Tasks & Deadlines:** List any specific actionable tasks or deadlines mentioned in the documents that are relevant to the meeting.
    3.  **Potential Talking Points:** Suggest 2-3 potential questions or topics for discussion based on the provided information.

    CONTEXT DOCUMENTS:
    ---
    {context}
    ---
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during Gemini briefing generation: {e}"