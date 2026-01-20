import argparse
import os
import subprocess
import sys
import shutil
import urllib.request
import re

# --- Utils ---

def run_notebooklm_cmd(args):
    cmd = ["notebooklm"] + args
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr.strip()}")
        return False
    print(f"✅ Success: {result.stdout.strip()}")
    return True

def is_url(s):
    return s.startswith("http://") or s.startswith("https://")

def is_downloadable(url):
    """Check if URL points to a file that needs downloading."""
    exts = ['.pdf', '.epub', '.docx', '.txt', '.md', '.csv']
    # Check extension or common download patterns
    return any(url.lower().endswith(ext) for ext in exts)

def download_file(url):
    print(f"⬇️ Downloading: {url}")
    filename = url.split('/')[-1] or "downloaded_file"
    # Basic sanitize
    filename = re.sub(r'[^\w\-.]', '_', filename)
    
    try:
        # User-Agent needed for some sites
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        
        print(f"Saved to: {filename}")
        return filename
    except Exception as e:
        print(f"Download failed: {e}")
        return None



# --- Z-Library Integration ---

def is_zlibrary_url(url):
    return any(d in url for d in ["z-lib.org", "zlib.li", "zlibrary", "1lib.sk", "art1lib.com"])

def handle_zlibrary(url):
    print(f"🕵️ Detected Z-Library Link: {url}")
    # Path to the specialized script
    zlib_script = "/Users/ge/Desktop/zlibrary-to-notebooklm/scripts/upload.py"
    
    if not os.path.exists(zlib_script):
        print("⚠️ Z-Library downloader script not found at expected path.")
        return False
        
    print("🚀 Delegating to specialized downloader (Z-Library)...")
    try:
        process = subprocess.Popen(
            [sys.executable, zlib_script, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"   [ZLib] {output.strip()}")
                
        if process.returncode == 0:
            print("✅ Z-Library book processed successfully.")
            return True
        else:
            print("❌ Z-Library downloader failed.")
            print(process.stderr.read())
            return False
    except Exception as e:
        print(f"❌ Error invoking Z-Library script: {e}")
        return False

# --- Anna's Archive Integration ---

def is_annas_url(url):
    return "annas-archive" in url or "annas-archive.li" in url or "annas-archive.org" in url

def handle_annas_archive(url):
    print(f"🕵️ Detected Anna's Archive Link: {url}")
    # Path to the specialized script
    # Note: Using absolute path based on user's known workspace structure
    annas_script = "/Users/ge/Desktop/annas-to-notebooklm/scripts/upload.py"
    
    if not os.path.exists(annas_script):
        print("⚠️ Anna's downloader script not found at expected path.")
        return False
        
    print("🚀 Delegating to specialized downloader (requires Playwright)...")
    try:
        # Utilizing the external script to handle download + upload
        # We capture output to show progress
        process = subprocess.Popen(
            [sys.executable, annas_script, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Stream output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"   [Annas] {output.strip()}")
                
        if process.returncode == 0:
            print("✅ Anna's Archive book processed successfully via external script.")
            return True
        else:
            print("❌ Anna's downloader failed.")
            print(process.stderr.read())
            return False
            
    except Exception as e:
        print(f"❌ Error invoking Anna's script: {e}")
        return False

# --- Main Logic ---

def main():
    parser = argparse.ArgumentParser(description="NotebookLM Universal Loader")
    parser.add_argument("inputs", nargs="+", help="URLs or File paths to upload")
    parser.add_argument("--notebook", "-n", help="Target Notebook Name")
    parser.add_argument("--download", "-d", action="store_true", help="Force download URL before upload")
    
    args = parser.parse_args()
    
    # 1. Check/Create Notebook (Skipped if delegating to Anna's script which creates its own)
    if args.notebook:
        print(f"Target Notebook: {args.notebook}")
        run_notebooklm_cmd(["create", args.notebook])
    
    # 2. Process Inputs
    for inp in args.inputs:
        
        # Case A: URL
        if is_url(inp):
            # Special Case 1: Anna's Archive
            if is_annas_url(inp):
                if handle_annas_archive(inp): continue
                print("⚠️ Falling back to default URL handling...")
            
            # Special Case 2: Z-Library
            if is_zlibrary_url(inp):
                if handle_zlibrary(inp): continue
                print("⚠️ Falling back to default URL handling...")

            # A-1: Download mode
            if args.download or is_downloadable(inp):
                local_path = download_file(inp)
                if local_path:
                    run_notebooklm_cmd(["source", "add", os.path.abspath(local_path)])
                    # Optional: clean up? os.remove(local_path)
            # A-2: Default URL mode
            else:
                print(f"🔗 Adding Link: {inp}")
                run_notebooklm_cmd(["source", "add", inp])
        
        # Case B: Local Path
        else:
            if os.path.exists(inp):
                # Folder (Recursive add)
                if os.path.isdir(inp):
                    print(f"📂 Scanning folder: {inp}")
                    for root, dirs, files in os.walk(inp):
                        for file in files:
                            if not file.startswith('.'): # Skip hidden
                                fpath = os.path.join(root, file)
                                print(f"  -> {file}")
                                run_notebooklm_cmd(["source", "add", os.path.abspath(fpath)])
                # Single File
                else:
                    print(f"📄 Adding File: {inp}")
                    run_notebooklm_cmd(["source", "add", os.path.abspath(inp)])
            else:
                print(f"⚠️ Not found: {inp}")

if __name__ == "__main__":
    main()
