# src/news_aggregator.py
import os
from tavily import TavilyClient
from .input_processor import process_url

# Initialize Tavily client using the API key from .env
try:
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
except Exception as e:
    print(f"Failed to initialize Tavily client: {e}")
    tavily_client = None

def get_latest_ai_news_content() -> str:
    """
    Searches for the latest AI news, scrapes the top results, 
    and returns all content as a single string.
    """
    if not tavily_client:
        raise ConnectionError("Tavily API client is not initialized. Check your TAVILY_API_KEY.")

    print("Searching for the latest AI news with Tavily...")
    
    # 1. Search for recent AI news
    # We use 'include_raw_content=True' to sometimes get content directly, saving a scrape call.
    search_results = tavily_client.search(
        query="Top AI news, breakthroughs, and developments this week in machine learning, LLMs, and artificial intelligence.",
        search_depth="advanced",
        max_results=7, # Get top 7 articles
        include_raw_content=False # We will scrape ourselves for consistency
    )
    
    all_news_content = ""
    scraped_urls = set()

    print(f"Found {len(search_results['results'])} potential articles.")

    # 2. Scrape each article
    for result in search_results['results']:
        url = result['url']
        if url in scraped_urls:
            continue # Avoid scraping the same URL twice

        try:
            print(f"Scraping news article: {url}")
            content = process_url(url)
            
            # 3. Combine the content
            all_news_content += f"--- START OF ARTICLE: {result['title']} ---\n"
            all_news_content += content
            all_news_content += f"\n--- END OF ARTICLE ---\n\n"
            
            scraped_urls.add(url)

        except Exception as e:
            print(f"Could not scrape article at {url}. Reason: {e}")
            continue # Move to the next article if one fails
    
    if not all_news_content:
        raise RuntimeError("Failed to gather any news content. All scraping attempts may have failed.")
        
    print("Finished aggregating all AI news content.")
    return all_news_content