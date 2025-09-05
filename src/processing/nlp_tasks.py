# Import the necessary libraries
from transformers import pipeline
import spacy

try:
  
    # This model is a smaller, faster version that provides great results.
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")

 
    nlp = spacy.load("en_core_web_sm")
    print("NLP models loaded successfully.")
except Exception as e:
    print(f"Error loading NLP models: {e}")
    summarizer = None
    nlp = None



def summarize_text(text: str, min_length: int = 40, max_length: int = 150) -> str:
    """
    Generates a concise summary for a given block of text, handling long inputs.
    """

    if not text or len(text.strip()) < min_length:
        return "The source text was too short or empty to generate a meaningful summary."


    if not summarizer:
        return "Summarizer model is not available."
    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        return "No text provided for summarization."
        
    try:
        # Model's max input size is 1024 tokens, we'll use a safe character limit
        max_chunk_size = 1000  # Characters per chunk
        overlap = 100          

        # Split the text into overlapping chunks
        chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size - overlap)]
        
        # Summarize each chunk
        individual_summaries = []
        for chunk in chunks:
            # For each chunk, we want a brief summary
            summary_result = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
            individual_summaries.append(summary_result[0]['summary_text'])
        
        # Combine the individual summaries into one text
        combined_summary_text = " ".join(individual_summaries)

        # If the combined summary is still very long, summarize it one last time
        if len(combined_summary_text) > max_chunk_size:
            final_summary_result = summarizer(combined_summary_text, max_length=max_length, min_length=min_length, do_sample=False)
            return final_summary_result[0]['summary_text']
        else:
            return combined_summary_text


    except IndexError:
        # This specific error happens if the model returns an empty sequence
        return "AI model could not generate a summary for this text."




    except Exception as e:
        return f"Error during summarization: {e}"

def extract_tasks_and_deadlines(text: str) -> dict:
    """
    Extracts potential tasks and deadlines from text using spaCy's NER.
    """
    if not nlp:
        return {"tasks": [], "deadlines": []}
    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        return {"tasks": [], "deadlines": []}

    doc = nlp(text)
    tasks = []
    deadlines = []
    
    # 1. A simple rule-based method for finding tasks.
    # We look for sentences containing action-oriented or request-based words.
    task_keywords = ["please", "task:", "action:", "review", "complete", "prepare", "send", "finalize"]
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in task_keywords):
            # Clean up the task sentence a bit
            tasks.append(sent.text.strip().replace("\n", " "))

    # 2. Use Named Entity Recognition (NER) to find dates and times.
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            deadlines.append(ent.text)
            
    return {"tasks": list(set(tasks)), "deadlines": list(set(deadlines))} # Use set to get unique items


# ----------------- SELF-TESTING BLOCK -----------------
# This allows us to run this file directly to test its functions.
if __name__ == '__main__':
    print("\n--- Testing NLP Functions ---")
    
    sample_text = """
    Hello Team,

    Just a reminder about a few key items for this week. 
    First, please review the Q3 financial report that Sarah sent out. We need all feedback by this Friday.
    Second, I have a new task: can someone please prepare the slides for the client presentation? The meeting is scheduled for next Tuesday at 3 PM.
    Finally, don't forget the team lunch tomorrow.

    Thanks,
    Alex
    """
    
    print("\n[1] Testing Summarization...")
    summary = summarize_text(sample_text)
    print(f"   Summary -> {summary}")
    
    print("\n[2] Testing Task and Deadline Extraction...")
    extracted_info = extract_tasks_and_deadlines(sample_text)
    print(f"   Extracted Info -> {extracted_info}")