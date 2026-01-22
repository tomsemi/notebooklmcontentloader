import argparse
import os
import sys

# Add the current directory to path so we can import 'core'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.utils import is_url, is_downloadable, download_file
from core.notebook_client import ensure_notebook, add_source
from core.providers import (
    is_annas_url, handle_annas_archive,
    is_zlibrary_url, handle_zlibrary
)

def main():
    parser = argparse.ArgumentParser(description="NotebookLM Universal Loader")
    parser.add_argument("inputs", nargs="+", help="URLs or File paths to upload")
    parser.add_argument("--notebook", "-n", help="Target Notebook Name")
    parser.add_argument("--download", "-d", action="store_true", help="Force download URL before upload")
    
    args = parser.parse_args()
    
    # 1. Check/Create Notebook
    if args.notebook:
        ensure_notebook(args.notebook)
    
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
                    add_source(local_path)
                    # Optional: clean up? os.remove(local_path)
            # A-2: Default URL mode
            else:
                print(f"🔗 Adding Link: {inp}")
                add_source(inp)
        
        # Case B: Local Path
        else:
            if os.path.exists(inp):
                inp = os.path.abspath(inp)
                # Folder (Recursive add)
                if os.path.isdir(inp):
                    print(f"📂 Scanning folder: {inp}")
                    for root, dirs, files in os.walk(inp):
                        for file in files:
                            if not file.startswith('.'): # Skip hidden
                                fpath = os.path.join(root, file)
                                print(f"  -> {file}")
                                add_source(fpath)
                # Single File
                else:
                    print(f"📄 Adding File: {inp}")
                    add_source(inp)
            else:
                print(f"⚠️ Not found: {inp}")

if __name__ == "__main__":
    main()
