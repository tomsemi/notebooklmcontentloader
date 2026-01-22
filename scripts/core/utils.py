import urllib.request
import re
import shutil
import os

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
         # Given this is a simple downloader, we accept what we get or maybe checking Content-Disposition header would be better
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
