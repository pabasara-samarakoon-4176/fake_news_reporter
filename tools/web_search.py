import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
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