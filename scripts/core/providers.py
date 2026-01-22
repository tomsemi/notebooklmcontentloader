import os
import subprocess
import sys

# --- Z-Library ---

def is_zlibrary_url(url):
    return any(d in url for d in ["z-lib.org", "zlib.li", "zlibrary", "1lib.sk", "art1lib.com", "z-lib.do", "singlelogin.re"])

def handle_zlibrary(url):
    print(f"🕵️ Detected Z-Library Link: {url}")
    zlib_script = "/Users/ge/Desktop/zlibrary-to-notebooklm/scripts/upload.py"
    
    if not os.path.exists(zlib_script):
        print(f"⚠️ Z-Library downloader script not found at {zlib_script}")
        return False
        
    print("🚀 Delegating to specialized downloader (Z-Library)...")
    return _run_external_script(zlib_script, url, "[ZLib]")

# --- Anna's Archive ---

def is_annas_url(url):
    return "annas-archive" in url or "annas-archive.li" in url or "annas-archive.org" in url

def handle_annas_archive(url):
    print(f"🕵️ Detected Anna's Archive Link: {url}")
    annas_script = "/Users/ge/Desktop/annas-to-notebooklm/scripts/upload.py"
    
    if not os.path.exists(annas_script):
        print(f"⚠️ Anna's downloader script not found at {annas_script}")
        return False
        
    print("🚀 Delegating to specialized downloader (requires Playwright)...")
    return _run_external_script(annas_script, url, "[Annas]")

# --- Helper ---

def _run_external_script(script_path, url, prefix):
    try:
        process = subprocess.Popen(
            [sys.executable, script_path, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"   {prefix} {output.strip()}")
                
        if process.returncode == 0:
            print(f"✅ {prefix} Processed successfully.")
            return True
        else:
            print(f"❌ {prefix} Failed.")
            print(process.stderr.read())
            return False
    except Exception as e:
        print(f"❌ Error invoking external script: {e}")
        return False
