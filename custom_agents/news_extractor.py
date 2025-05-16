from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
# from tools.extract_news_from_url import extract_news_from_url

MODEL_GPT_4O = "openai/gpt-4o"

from newspaper import Article
from tools import web_search, fact_check

def extract_news_from_url(url) -> dict:
    """
    Extracts the title and text from a news article given its URL.

    Args:
        url (str): The URL of the news article.

    Returns:
        dict: A dictionary containing the title and text of the article.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()

        return {
            "title": article.title,
            "text": article.text
        }
    except Exception as e:
        print(f"An error occurred while extracting news from URL: {e}")
        return None

news_extractor = Agent(
    name="news_extractor",
    description="Extracts news articles from URLs.",
    tools=[extract_news_from_url],
    model=LiteLlm(model=MODEL_GPT_4O)
)