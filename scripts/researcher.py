import argparse
import os
import sys

# Path setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.notebook_client import ensure_notebook, add_source, ask_question
from core.utils import is_url, download_file, is_downloadable

def main():
    parser = argparse.ArgumentParser(description="NotebookLM AI Researcher")
    parser.add_argument("--notebook", "-n", help="Target Notebook Name (Required for research context)")
    parser.add_argument("--query", "-q", help="The question or prompt to ask")
    parser.add_argument("--source", "-s", help="Optional: Quick add a URL or file before asking")
    parser.add_argument("--output", "-o", help="Save the answer to this file (e.g., report.md)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Enter interactive chat mode")
    
    args = parser.parse_args()

    # 1. Setup Notebook
    current_nb = args.notebook
    if current_nb:
        success, _ = ensure_notebook(current_nb)
        if not success:
            print("❌ Failed to set notebook context.")
            return
    else:
        print("ℹ️ No notebook specified. Using current context.")

    # 2. Add Source (Optional)
    if args.source:
        inp = args.source
        print(f"📥 Adding source: {inp}")
        
        # Simple Logic reusing parts of loader (simplified)
        if is_url(inp):
            if is_downloadable(inp): # Simple check
                local = download_file(inp)
                if local: add_source(local)
            else:
                add_source(inp)
        else:
            add_source(os.path.abspath(inp))

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
