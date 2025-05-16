from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("FACT_CHECK_API_KEY")

if not api_key:
    raise ValueError("Please set the FACT_CHECK_API_KEY environment variable.")

def search_claims(query):
    """
    Perform a fact check using the Google Fact Check API.

    Args:
        query (str): The search query.

    Returns:
        list: A list of fact check results.
    """
    try:
        service = build("factchecktools", "v1alpha1", developerKey=api_key)
        request = service.claims().search(query=query)
        response = request.execute()
        return response.get("claims")
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
if __name__ == "__main__":
    query = "COVID-19 vaccine effectiveness"
    results = search_claims(query)
    print(results[0])
       