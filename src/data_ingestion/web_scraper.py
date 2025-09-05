import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

# --- IMPORTANT ---
# Update this path to where you placed msedgedriver.exe
EDGE_DRIVER_PATH = r"C:\Users\sp445\Downloads\edgedriver_win64\msedgedriver.exe"

def fetch_and_clean_url(url: str) -> str:
    """
    Fetches content using Selenium and uses an advanced method
    to find the main article text, filtering out navigation and junk.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    service = Service(EDGE_DRIVER_PATH)
    
    try:
        with webdriver.Edge(service=service, options=options) as driver:
            driver.set_page_load_timeout(20)
            try:
                driver.get(url)
            except Exception:
                print("Page load timed out, proceeding with content.")
            page_source = driver.page_source
        
        soup = BeautifulSoup(page_source, 'html.parser')
        
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        main_content = ""
        max_text_len = 0
        potential_containers = soup.find_all(['article', 'main', 'div'])
        
        for container in potential_containers:
            text = container.get_text(separator=' ', strip=True)
            if len(text) > max_text_len and '.' in text:
                max_text_len = len(text)
                main_content = text
        
        if not main_content:
            return "Could not extract the main article text from this page."

        return main_content

    except Exception as e:
        print(f"An error occurred with Selenium: {e}")
        return f"Error: Could not process the URL. Check the EdgeDriver path and URL."