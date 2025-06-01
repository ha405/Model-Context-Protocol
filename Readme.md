# Model Context Protocol (MCP)


A system for automatically generating documentation and answering questions about code repositories using Large Language Models (LLMs). It provides a JSON-RPC interface for accessing repository content and uses the Gemini API for natural language processing.

## 🚀 Features

- **Automated README Generation**: Generate comprehensive documentation from your codebase
- **Code Context Retrieval**: Access and analyze GitHub repository content through a JSON-RPC API
- **RAG-based Question Answering**: Ask questions about your codebase using retrieval-augmented generation
- **Flexible Architecture**: Modular design with separate server and client components

## 📋 Prerequisites

- Node.js (for the server)
- Python 3.10+ (for the client)
- Gemini API key
- Git

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Model-Context-Protocol.git
cd Model-Context-Protocol
```

2. Install server dependencies:
```bash
cd mcp-server
npm install
```

3. Install client dependencies:
```bash
cd ../client
pip install requests google-generativeai tqdm
```

4. Set up your Gemini API key:
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```

Here's a breakdown:

**1. `mcp-server` (GitHub Repository Content Server):**

*   **Purpose:**  Serves file contents from a specified GitHub repository. It acts as a simple API, offering methods to list files and retrieve their content.
*   **Key Components:**
    *   `config.js`:  Configuration file.  Defines the target GitHub repository (owner, repository name, branch) from which files are fetched.
    *   `rpc_handler.js`:  Handles the JSON-RPC requests.
        *   `/initialize`:  A dummy endpoint to demonstrate the server's capabilities
        *   `resources/list`:  Retrieves a list of files from the GitHub repository (filtered by supported extensions, currently just `.py`).  Returns an array of file metadata including URI and name.
        *   `resources/fetch`:  Retrieves the content of a specific file based on its URI.  Fetches the raw content from GitHub and returns it.
    *   `server.js`:  The HTTP server.  Listens for POST requests to `/rpc`. It parses the request body as JSON, passes it to the `handleRpcRequest` function, and returns the response as JSON.  Implements error handling and basic HTTP 404 handling for non-`/rpc` requests.
*   **Functionality:**
    *   Exposes a JSON-RPC API.
    *   Fetches file lists and content from GitHub using the GitHub API and raw content URLs.
    *   Filters files based on supported extensions.
    *   Provides a structured JSON response with file metadata and content.

**2. `client` (README Generator Client):**

*   **Purpose:**  Orchestrates the process of gathering file contents and using an LLM to generate a README file.
*   **Key Components:**
    *   `MCPClient`:  A class that handles communication with the server. It encapsulates the logic for sending JSON-RPC requests.
        *   `__init__`: Initializes the class with the server's URL.
        *   `send_request`: Constructs a JSON-RPC request, sends it to the server using `requests`, and returns the JSON response.
    *   `generate_response`:  Uses the Gemini LLM (through the `google-generativeai` library) to generate text based on a given prompt.
    *   `main`:
        *   Initializes an `MCPClient` to connect to the local server.
        *   Calls `resources/list` to get a list of files.
        *   Iterates through the files, calling `resources/fetch` for each one to get its content.
        *   Concatenates all the file contents into a single string, adding a header for each file.
        *   Constructs a prompt for the LLM, asking it to generate a README based on the combined file content.
        *   Calls `generate_response` to get the LLM-generated README text.
        *   Writes the generated README to a file named `GENERATED_README.md` in the same directory as the script.
*   **Functionality:**
    *   Communicates with the `mcp-server` to retrieve file contents.
    *   Constructs a prompt for the LLM based on the retrieved content.
    *   Uses the Gemini LLM to generate a README file.
    *   Writes the generated README file to disk.

## 🔧 Usage

### Starting the Server

1. Start the MCP server:
```bash
cd mcp-server
node server.js
```
The server will start on http://localhost:4000 by default.

### Generating Documentation

To generate a README for a GitHub repository:

```powershell
cd client
python client.py --owner "username" --repo "repository-name" --branch "main"
```

Options:
- `--owner`: GitHub username/organization (required)
- `--repo`: Repository name (required)
- `--branch`: Git branch name (default: main)
- `--output`: Output file path (default: GENERATED_README.md)
- `--repo-name`: Custom repository name for README title

### Using the RAG System

Ask questions about your codebase:

```powershell
cd rag
python app.py --owner "username" --repo "repository-name"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 How It Works

The system operates in three main components:

1. **MCP Server** (`mcp-server/`)
   - Provides JSON-RPC API for repository access
   - Handles file listing and content retrieval
   - Supports multiple file types and repositories

2. **Documentation Generator** (`client/`)
   - Fetches repository content through MCP server
   - Processes code and generates documentation
   - Uses Gemini API for natural language generation

3. **RAG System** (`rag/`)
   - Implements retrieval-augmented generation
   - Answers questions about the codebase
   - Uses semantic search for relevant context