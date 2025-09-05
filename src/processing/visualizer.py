# from wordcloud import WordCloud, STOPWORDS
# import matplotlib.pyplot as plt

# def generate_word_cloud(text: str):
#     """
#     Generates a word cloud visualization from text if the text is substantial.
#     Cleans the text by removing common stop words.

#     Args:
#         text (str): The full text to analyze.

#     Returns:
#         A matplotlib Figure object if a cloud is generated, otherwise None.
#     """
#     # 1. Check if the text is long enough for a meaningful visualization
#     if len(text.split()) < 50: # Require at least 50 words
#         print("Text too short for word cloud, skipping.")
#         return None

#     # 2. Add custom stop words to the default list to filter out noise
#     custom_stopwords = set(STOPWORDS)
#     custom_stopwords.update([
#         "will", "said", "go", "one", "may", "report", "document",
#         "text", "file", "page", "content", "information"
#     ])

#     # 3. Generate the word cloud
#     try:
#         wordcloud = WordCloud(
#             width=800,
#             height=400,
#             background_color='white',
#             stopwords=custom_stopwords,
#             colormap='viridis', # A nice color scheme
#             min_font_size=10
#         ).generate(text)

#         # 4. Create a matplotlib figure to display it
#         fig, ax = plt.subplots(figsize=(10, 5))
#         ax.imshow(wordcloud, interpolation='bilinear')
#         ax.axis('off') # Hide the axes
#         plt.tight_layout(pad=0)
        
#         return fig

#     except Exception as e:
#         print(f"Error generating word cloud: {e}")
#         return None


from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import re
from collections import Counter

def generate_word_cloud(text: str, max_words: int = 50):
    """
    Generates a cleaner, more meaningful word cloud visualization from text.
    Filters out common stop words and low-value terms.

    Args:
        text (str): The full text to analyze.
        max_words (int): Maximum number of top words to visualize.

    Returns:
        A matplotlib Figure object if a cloud is generated, otherwise None.
    """
    # 1. Quick check: avoid wasting time on tiny docs
    if len(text.split()) < 50:
        print("Text too short for word cloud, skipping.")
        return None

    # 2. Normalize text (lowercase + remove numbers/symbols)
    clean_text = re.sub(r"[^a-zA-Z\s]", "", text.lower())

    # 3. Extended stopwords list
    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update([
        "will", "said", "go", "one", "may", "report", "document",
        "text", "file", "page", "content", "information", 
        "data", "value", "analysis", "use", "used", "example"
    ])

    # 4. Tokenize and filter stopwords
    words = [w for w in clean_text.split() if w not in custom_stopwords and len(w) > 2]

    if not words:
        print("No meaningful words found after cleaning.")
        return None

    # 5. Keep only the top `max_words` most frequent terms
    freq_dist = Counter(words)
    most_common_words = dict(freq_dist.most_common(max_words))

    # 6. Generate word cloud using filtered frequencies
    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="viridis",
            min_font_size=12
        ).generate_from_frequencies(most_common_words)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        plt.tight_layout(pad=0)

        return fig

    except Exception as e:
        print(f"Error generating word cloud: {e}")
        return None
