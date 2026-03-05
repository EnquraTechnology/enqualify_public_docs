import os
import requests
from markdownify import markdownify as md

# Yapılandırma
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "https://enqura.atlassian.net")
EMAIL = os.environ.get("CONFLUENCE_EMAIL")
API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN")
SPACE_KEY = "EDP"
LABEL = "customer-visible"

def get_pages_by_label():
    cql = f'space = "{SPACE_KEY}" AND label = "{LABEL}"'
    url = f"{CONFLUENCE_URL}/wiki/rest/api/content/search"
    auth = (EMAIL, API_TOKEN)
    params = {'cql': cql, 'expand': 'body.storage'}
    
    response = requests.get(url, auth=auth, params=params)
    response.raise_for_status()
    return response.json()['results']

def sync():
    pages = get_pages_by_label()
    if not os.path.exists('docs'):
        os.makedirs('docs')

    for page in pages:
        title = page['title'].replace("/", "-")
        html_content = page['body']['storage']['value']
        markdown_content = md(html_content)
        
        file_path = f"docs/{title}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {page['title']}\n\n")
            f.write(markdown_content)
        print(f"Senkronize edildi: {title}")

if __name__ == "__main__":
    sync()
