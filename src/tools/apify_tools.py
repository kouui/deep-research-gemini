
import os
from dotenv import load_dotenv
import requests

class ApifyRagWebBrowser:
    def __init__(self):
        load_dotenv()
        token = os.getenv('APIFY_API_KEY')
        self.base_url = f"https://api.apify.com/v2/acts/apify~rag-web-browser/run-sync-get-dataset-items?token={token}"

    def fetch_web_content(self, search_query: str, memory:int=4096, timeout:int=180) :
        """Fetch web content using Apify's RAG Web Browser actor."""
        url = f"{self.base_url}&memory={memory}&timeout={timeout}"
        body = {"query": search_query}
        response = requests.get(url, json=body)

        data = response.json()  # len=3 list of dict
        """
        (Pdb) len(data)  
        3
        (Pdb) data[0].keys()
        dict_keys(['crawl', 'searchResult', 'metadata', 'text'])
        """
        return [d for d in data if d["crawl"]["requestStatus"] == "handled" and d.get("markdown","")]