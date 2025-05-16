from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.agents import SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import os
from newspaper import Article
import requests
import json
from googleapiclient.discovery import build

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_GPT_4O = "openai/gpt-4o"

FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY")

if not FACT_CHECK_API_KEY:
    raise ValueError("Please set the FACT_CHECK_API_KEY environment variable.")

def search_claims(query: str) -> list:
    """
    Perform a fact check using the Google Fact Check API.

    Args:
        query (str): The search query.

    Returns:
        list: A list of fact check results.
    """
    try:
        service = build("factchecktools", "v1alpha1", developerKey=FACT_CHECK_API_KEY)
        request = service.claims().search(query=query)
        response = request.execute()
        return response.get("claims")
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not SERPER_API_KEY:
    raise ValueError("Please set the SERPER_API_KEY environment variable.")

def search_web(query: str) -> list:
    """
    Perform a web search using the Serper API.

    Args:
        query (str): The search query.

    Returns:
        list: A list of search results.
    """
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "q": query
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("organic", [])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def extract_news_from_url(url: str) -> dict:
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
    instruction="You are a helpfull assistant who can extract news stories from given URLs.",
    description="Extracts news articles from URLs.",
    tools=[extract_news_from_url],
    model=LiteLlm(model=MODEL_GPT_4O)
)

verifier = Agent(
    name="verifier",
    instruction="You are a helpful assistant who can verify news stories by fact checking. You can use web search as a fallback if you cannot find the information in the fact check API.",
    description="Verifies news articles by fact checking.",
    tools=[search_claims, search_web],
    model=LiteLlm(model=MODEL_GPT_4O)
)

reporter = LlmAgent(
    name="reporter",
    description="Extracts and verifies news articles.",
    instruction="""
    You are a fact-checking report generator.
    Your task is to write a clear and concise report evaluating the accuracy of news articles, based on its content and available fact-checking results.
    """,
    model=LiteLlm(model=MODEL_GPT_4O)
)

pipeline_agent = SequentialAgent(
    name="pipeline_agent",
    sub_agents=[news_extractor, verifier, reporter],
    description="Executes a sequence of news extraction, verification, and reporing."
)

root_agent = pipeline_agent