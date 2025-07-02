# src/input_processor.py
import logging
from typing import Optional
import pypdf
from firecrawl import FirecrawlApp
from . import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_pdf(file_path: str) -> Optional[str]:
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        Optional[str]: Extracted text or None if processing fails.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the file is not a valid PDF or cannot be processed.
    """
    logger.info(f"Processing PDF: {file_path}")
    try:
        with open(file_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            if not reader.pages:
                logger.warning("PDF contains no pages")
                return None
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
                else:
                    logger.warning(f"Could not extract text from page in {file_path}. Page may be scanned or empty.")
            if not text.strip():
                logger.warning("No text extracted from PDF. It may be scanned or contain only images.")
                return None
            return text.strip()
    except FileNotFoundError:
        logger.error(f"PDF file not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error processing PDF {file_path}: {str(e)}")
        raise ValueError(f"Failed to process PDF: {str(e)}")

# In src/input_processor.py

# ... (keep the other imports and the process_pdf/process_prompt functions) ...
# In src/input_processor.py

# ... (imports and other functions remain the same) ...
from firecrawl import FirecrawlApp
from . import config

# In src/input_processor.py

# ... (imports and other functions remain the same) ...
from firecrawl import FirecrawlApp
from . import config

# In src/input_processor.py

# ... (imports and other functions remain the same) ...
from firecrawl import FirecrawlApp
from . import config

# In src/input_processor.py

# ... (imports and other functions remain the same) ...
from firecrawl import FirecrawlApp
from . import config

def process_url(url: str) -> str:
    """
    Scrapes a URL for its main content using Firecrawl and correctly handles
    the ScrapeResponse object returned by the SDK.
    """
    print(f"Scraping URL with the correct object handling: {url}")
    
    try:
        app = FirecrawlApp(api_key=config.FIRE_CRAWL_API_KEY)
        
        # This is the simplest, correct call.
        scrape_result = app.scrape_url(url)
        
        # --- THE CORRECT WAY TO ACCESS THE DATA ---
        # The result is an object, so we access its 'markdown' attribute.
        if scrape_result and hasattr(scrape_result, 'markdown') and scrape_result.markdown:
            print("Successfully extracted markdown content from the ScrapeResponse object.")
            return scrape_result.markdown
        else:
            # This handles cases where the scrape succeeded but returned no markdown content.
            print(f"Firecrawl scrape was successful, but the response object had no markdown content. Full response: {scrape_result}")
            raise RuntimeError(
                "Firecrawl was unable to extract text from this URL. "
                "The site may be heavily protected or have an unusual layout."
            )
            
    except Exception as e:
        # Catch API errors or our custom RuntimeErrors
        print(f"An error occurred during the Firecrawl process: {e}")
        raise RuntimeError(f"Failed to scrape URL. Firecrawl error: {e}")

def process_prompt(prompt: str) -> Optional[str]:
    """
    Processes a user-provided prompt.

    Args:
        prompt (str): The user input prompt.

    Returns:
        Optional[str]: The prompt if valid, None if empty or invalid.

    Raises:
        ValueError: If the prompt is not a valid string.
    """
    logger.info(f"Processing prompt: '{prompt}'")
    try:
        if not isinstance(prompt, str):
            logger.error("Prompt must be a string")
            raise ValueError("Prompt must be a string")
        if not prompt.strip():
            logger.warning("Empty prompt provided")
            return None
        return prompt.strip()
    except Exception as e:
        logger.error(f"Error processing prompt: {str(e)}")
        raise ValueError(f"Failed to process prompt: {str(e)}")