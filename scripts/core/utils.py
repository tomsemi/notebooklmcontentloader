import urllib.request
import re
import shutil
import os
import requests
from bs4 import BeautifulSoup

def is_url(s):
    return s.startswith("http://") or s.startswith("https://")

def is_downloadable(url):
    """Check if URL points to a file that needs downloading."""
    exts = ['.pdf', '.epub', '.docx', '.txt', '.md', '.csv']
    return any(url.lower().endswith(ext) for ext in exts) or "/slow_download/" in url

def download_file(url):
    print(f"⬇️ Downloading: {url}")
    filename = url.split('/')[-1]
    # Handle cases where filename is empty or weird
    if not filename or len(filename) > 255:
        filename = "downloaded_file"
        
    # Basic sanitize
    filename = re.sub(r'[^\w\-.]', '_', filename)
    if not filename.endswith((".pdf", ".epub", ".docx", ".txt", ".md")):
         # Try to guess or just append nothing, risking it. 
         # For now, keep it simple as per original script
         pass

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        
        print(f"Saved to: {filename}")
        return os.path.abspath(filename)
    except Exception as e:
        print(f"Download failed: {e}")
        return None

def download_url_content(url):
    """
    Fetches the content of a URL and saves it as a local Markdown file.
    Used as a fallback when NotebookLM fails to process a URL directly.
    """
    print(f"🕷️  Crawling content from: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()

        # Get text
        title = soup.title.string if soup.title else "Extracted Content"
        text = soup.get_text(separator='\n\n')
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Create a filename
        safe_title = re.sub(r'[^\w\-]', '_', title)[:50]
        filename = f"{safe_title}.txt" # Use .txt for simplicity, it's safer for NotebookLM than .md sometimes
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Source URL: {url}\n\n")
            f.write(f"# {title}\n\n")
            f.write(text)
            
        print(f"✅ Content saved to local file: {filename}")
        return os.path.abspath(filename)
        
    except Exception as e:
        print(f"❌ Failed to crawl URL: {e}")
        return None
