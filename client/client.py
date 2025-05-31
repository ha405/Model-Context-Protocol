# client.py
import requests
import json
from google import genai
import os

client = genai.Client(api_key="AIzaSyBoAFOxBSX1nxEF8lNuhJudPiHVTCRNK8Q")

def generate_response(contents):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=contents
    )
    return response.text.strip()

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
        response = requests.post(self.url, json=req)
        self.request_id += 1
        return response.json()

def main():
    server_url = "http://localhost:4000/rpc"
    mcp = MCPClient(server_url)

    list_resp = mcp.send_request("resources/list")
    files = list_resp.get("result", [])

    combined_content = ""
    for file in files:
        uri = file["uri"]
        fetch_resp = mcp.send_request("resources/fetch", {"uri": uri})
        content = fetch_resp["result"]["content"]
        combined_content += f"\n\n### {file['name']}\n\n{content}"

    prompt = f"Generate a comprehensive README in Markdown format for this repository. Use the following file contents as reference:\n{combined_content}"
    readme_text = generate_response([prompt])

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "GENERATED_README.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme_text)

if __name__ == "__main__":
    main()
