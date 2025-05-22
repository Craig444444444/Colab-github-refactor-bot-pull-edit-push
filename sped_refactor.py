import os
import openai
import subprocess
from typing import Dict, Callable

# Setup OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set your OPENAI_API_KEY environment variable")

# Example: agents dictionary to hold refactor functions
def openai_refactor_code(original_code: str) -> str:
    prompt = (
        "You are a professional software engineer and code refactoring assistant. "
        "Improve the following Python code to make it cleaner, more efficient, and follow best practices. "
        "Preserve the original functionality.\n\n"
        "Original code:\n"
        f"{original_code}\n\n"
        "Refactored code:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500,
    )
    refactored_code = response['choices'][0]['message']['content'].strip()
    return refactored_code

agents: Dict[str, Callable[[str], str]] = {
    "OpenAI_GPT_Refactor": openai_refactor_code,
    # Add more agents if you want
}

# Your code file path (to be refactored)
CODE_FILE_PATH = "your_code.py"

def read_code(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_code(file_path: str, code: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

def run_agents_and_collect_results(code: str) -> Dict[str, str]:
    results = {}
    for agent_name, refactor_func in agents.items():
        print(f"Running agent: {agent_name}")
        try:
            result = refactor_func(code)
            results[agent_name] = result
        except Exception as e:
            print(f"Agent {agent_name} failed with error: {e}")
    return results

def save_results_to_files(results: Dict[str, str], base_filename="refactor_output"):
    for agent_name, code in results.items():
        filename = f"{base_filename}_{agent_name}.py"
        print(f"Saving refactored code from {agent_name} to {filename}")
        write_code(filename, code)

def git_commit_and_push(commit_message: str):
    print("Adding files to git")
    subprocess.run(["git", "add", "."], check=True)
    print(f"Committing with message: {commit_message}")
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print("Pushing to origin")
    subprocess.run(["git", "push", "origin", "main"], check=True)

def main():
    original_code = read_code(CODE_FILE_PATH)
    results = run_agents_and_collect_results(original_code)
    save_results_to_files(results)
    git_commit_and_push("Auto refactor update from SPEDitor")

if __name__ == "__main__":
    main()
