import argparse
import os
import sys

# Path setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.notebook_client import ensure_notebook, add_source, ask_question, wait_for_source
from core.utils import is_url, download_file, is_downloadable, download_url_content

def main():
    parser = argparse.ArgumentParser(description="NotebookLM AI Researcher")
    parser.add_argument("--notebook", "-n", help="Target Notebook Name (Required for research context)")
    parser.add_argument("--query", "-q", help="The question or prompt to ask")
    parser.add_argument("--source", "-s", help="Optional: Quick add a URL or file before asking")
    parser.add_argument("--output", "-o", help="Save the answer to this file (e.g., report.md)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Enter interactive chat mode")
    
    args = parser.parse_args()

    # 1. Setup Notebook
    current_nb = None
    if args.notebook:
        success, nb_id = ensure_notebook(args.notebook)
        if success and nb_id:
            current_nb = nb_id
            print(f"✅ Context set to Notebook ID: {current_nb}")
        else:
            print("❌ Failed to set notebook context (Could not create or retrieve ID).")
            return
    else:
        print("ℹ️ No notebook specified. Using current context.")

    # 2. Add Source (Optional)
    if args.source:
        inp = args.source
        print(f"📥 Adding source: {inp}")
        
        source_id = None
        success = False

        # Simple Logic reusing parts of loader (simplified)
        if is_url(inp):
            if is_downloadable(inp): # Simple check
                local = download_file(inp)
                if local: 
                    success, source_id = add_source(local, notebook=current_nb)
            else:
                # Try adding as URL first
                success, source_id = add_source(inp, notebook=current_nb)
                
                # Fallback: If URL add failed, try crawling
                if not success:
                    print("⚠️ URL Direct Add Failed. Attempting to crawl content...")
                    local_content = download_url_content(inp)
                    if local_content:
                        success, source_id = add_source(local_content, notebook=current_nb)
                    else:
                        print("❌ Crawling also failed.")

        else:
            success, source_id = add_source(os.path.abspath(inp), notebook=current_nb)

        if success:
            if source_id:
                print(f"⏳ Waiting for source processing (ID: {source_id})...")
                wait_for_source(source_id, notebook=current_nb)
                print("✅ Source is ready.")
            else:
                print("⚠️ Source added but ID not returned. Skipping wait (query might fail).")
        else:
            print("❌ Failed to add source.")

    # 3. Ask Query
    if args.query:
        print(f"🤖 Asking AI: {args.query}...")
        success, answer = ask_question(args.query, notebook=current_nb)
        
        if success:
            print("\n" + "="*40)
            print(answer)
            print("="*40 + "\n")
            
            if args.output:
                with open(args.output, "w") as f:
                    f.write(f"# Question: {args.query}\n\n")
                    f.write(answer)
                print(f"💾 Report saved to: {args.output}")
        else:
            print("❌ Query failed.")

    # 4. Interactive Mode
    if args.interactive:
        print("💬 Entering Interactive Mode (Ctrl+C to exit)")
        while True:
            try:
                q = input("\n[You]: ")
                if not q.strip(): continue
                if q.lower() in ['exit', 'quit']: break
                
                success, answer = ask_question(q, notebook=current_nb)
                if success:
                    print(f"[AI]: {answer}")
                else:
                    print("❌ Error fetching answer")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == "__main__":
    main()
