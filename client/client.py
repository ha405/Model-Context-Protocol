import requests
import json
from google import genai
import os
import argparse
from tqdm import tqdm

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(api_key=api_key)

def summarize_all_files(file_data, repo_name=None):
    title = f"Repository: {repo_name}\n\n" if repo_name else ""
    prompt = title + "Summarize the purpose and functionality of the following codebase:\n\n"

    for file in file_data:
        prompt += f"---\nFile: {file['name']}\nContent:\n{file['content']}\n\n"

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=[prompt]
    )
    return response.text.strip()

def generate_readme_from_summary(summary, repo_name=None):
    title = f"# {repo_name} Repository\n\n" if repo_name else "# Project README\n\n"
    return title + summary

class MCPClient:
    def __init__(self, url):
        self.url = url
        self.request_id = 1

    def send_request(self, method, params=None):
        req = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method
        }
        if params is not None:
            req["params"] = params
        res = requests.post(self.url, json=req)
        self.request_id += 1
        return res.json()

def main():
    parser = argparse.ArgumentParser(description="Generate README from MCP repo")
    parser.add_argument("--server-url", type=str, default="http://model-context-protocol-production.up.railway.app/rpc")
    parser.add_argument("--owner", type=str, required=True)
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--branch", type=str, default="main")
    parser.add_argument("--output", type=str, default="GENERATED_README.md")
    parser.add_argument("--repo-name", type=str)
    args = parser.parse_args()

    mcp = MCPClient(args.server_url)
    mcp.send_request("initialize", {"owner": args.owner, "repo": args.repo, "branch": args.branch})

    list_resp = mcp.send_request("resources/list")
    files = list_resp.get("result", [])

    file_data = []
    print("📥 Fetching all files...")
    for file in tqdm(files, desc="Fetching files", unit="file"):
        uri = file["uri"]
        fetch_resp = mcp.send_request("resources/fetch", {"uri": uri})
        content = fetch_resp["result"]["content"]
        file_data.append({"name": file["name"], "content": content})

    print("🧠 Summarizing codebase...")
    summary = summarize_all_files(file_data, repo_name=args.repo_name)

    print("📝 Generating README...")
    readme_text = generate_readme_from_summary(summary, repo_name=args.repo_name)
    output_path = os.path.join(os.getcwd(), args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme_text)

    print(f"✅ README generated: {output_path}")

if __name__ == "__main__":
    main()
