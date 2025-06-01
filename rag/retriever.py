# retriever.py
import requests

class MCPClient:
    def __init__(self, url="http://localhost:4000/rpc"):
        self.url = url
        self.request_id = 1

    def send_request(self, method, params=None):
        req = {"jsonrpc": "2.0", "id": self.request_id, "method": method}
        if params is not None:
            req["params"] = params
        res = requests.post(self.url, json=req)
        self.request_id += 1
        return res.json()

class Retriever:
    def __init__(self, server_url="http://localhost:4000/rpc"):
        self.mcp = MCPClient(server_url)

    def initialize(self, owner, repo, branch="main"):
        self.mcp.send_request("initialize", {"owner": owner, "repo": repo, "branch": branch})

    def get_text_files(self):
        list_resp = self.mcp.send_request("resources/list")
        files = list_resp.get("result", [])
        return [f for f in files if f["name"].endswith(('.py', '.js', '.ts', '.jsx', '.tsx'))]

    def fetch_file_content(self, uri):
        fetch_resp = self.mcp.send_request("resources/fetch", {"uri": uri})
        return fetch_resp["result"]["content"]

    def chunk_text(self, text, chunk_size=300, overlap=50):
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += chunk_size - overlap
        return chunks

    def load_and_chunk_files(self, chunk_size=300, overlap=50):
        all_chunks = []
        files = self.get_text_files()
        for f in files:
            uri = f["uri"]
            name = f["name"]
            content = self.fetch_file_content(uri)
            pieces = self.chunk_text(content, chunk_size, overlap)
            for idx, piece in enumerate(pieces):
                all_chunks.append({"uri": uri, "name": name, "index": idx, "chunk": piece})
        return all_chunks
