# src/input_processor.py
import pypdf
from firecrawl import FirecrawlApp
from . import config

def process_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    print(f"Processing PDF: {file_path}")
    text = ""
    with open(file_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def process_url(url: str) -> str:
    """Scrapes a URL for its main content using Firecrawl."""
    print(f"Scraping URL: {url}")
    app = FirecrawlApp(api_key=config.FIRE_CRAWL_API_KEY)
    scraped_data = app.scrape_url(url)
    # We only want the core content, not all the metadata.
    return scraped_data['content']

def process_prompt(prompt: str) -> str:
    """Simply returns the user's prompt."""
    print(f"Processing prompt: '{prompt}'")
    return prompt