def load_web_content(url):
    import requests
    from bs4 import BeautifulSoup

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the HTML
        text = soup.get_text(separator=' ', strip=True)
        return text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to load content from {url}: {e}")