from newspaper import Article

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