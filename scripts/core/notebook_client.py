import subprocess
import json

def run_notebooklm_cmd(args):
    """
    Runs a notebooklm command and returns (success, output).
    If output is expected to be JSON (determined by args), it tries to parse it? 
    For now, just return raw stdout string.
    """
    cmd = ["notebooklm"] + args
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr.strip()}")
            return False, result.stderr.strip()
        # print(f"✅ Success: {result.stdout.strip()[:100]}...") # Log less
        return True, result.stdout.strip()
    except FileNotFoundError:
        print("❌ Error: 'notebooklm' command not found. Please install notebooklm-py.")
        return False, "Command not found"

def ensure_notebook(notebook_name):
    """Creates a notebook if it doesn't exist, or switches to it."""
    # Note: notebooklm CLI 'create' switches context to it.
    print(f"Target Notebook: {notebook_name}")
    # We use 'create' which likely gets or creates. 
    # Actually checking `notebooklm create --help` might be useful, but based on loader.py it was just running create.
    # The CLI behavior: create switches to the new notebook.
    return run_notebooklm_cmd(["create", notebook_name])

def add_source(source_path):
    return run_notebooklm_cmd(["source", "add", source_path])

def ask_question(question, notebook=None):
    args = ["ask", question]
    if notebook:
        args.extend(["-n", notebook])
    return run_notebooklm_cmd(args)
