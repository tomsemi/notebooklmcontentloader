import subprocess
import json
import re

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
    """
    Creates a notebook and returns (success, notebook_id).
    """
    print(f"Target Notebook: {notebook_name}")
    # Always create for now since list is unreliable.
    # Users effectively get a new research session per run if using this.
    success, output = run_notebooklm_cmd(["create", notebook_name])
    
    if success:
        # Expected output: "Created notebook: UUID - Name"
        match = re.search(r"Created notebook:\s*([0-9a-fA-F-]+)", output)
        if match:
            return True, match.group(1)
        else:
            print(f"⚠️ Warning: Could not parse Notebook ID from: {output}")
            # Fallback: maybe it didn't print standard output? Return name as last resort?
            # No, returning name fails RPCs. Return None.
            return True, None # Proceed with caution or fail?
    return False, None

def add_source(source_path, notebook=None):
    """
    Adds a source to the specified (or current) notebook.
    Returns (success, source_id).
    """
    args = ["source", "add", source_path, "--json"]
    if notebook:
        args.extend(["-n", notebook])
    
    success, output = run_notebooklm_cmd(args)
    if success:
        try:
            data = json.loads(output)
            source_id = data.get("source", {}).get("id")
            return True, source_id
        except json.JSONDecodeError:
            print(f"⚠️ Warning: Could not parse JSON output: {output}")
            return True, None
    return False, None

def wait_for_source(source_id, notebook=None, timeout=120):
    """Waits for a source to leverage the 'source wait' command."""
    args = ["source", "wait", source_id, "--timeout", str(timeout)]
    if notebook:
        args.extend(["-n", notebook])
    return run_notebooklm_cmd(args)

def ask_question(question, notebook=None):
    args = ["ask", question]
    if notebook:
        args.extend(["-n", notebook])
    return run_notebooklm_cmd(args)
