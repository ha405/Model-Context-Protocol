import fetch from 'node-fetch';
import { githubRepo } from './config.js';

const supportedExtensions = ['.txt', '.py'];

const githubApiUrl = `https://api.github.com/repos/${githubRepo.owner}/${githubRepo.repo}/git/trees/${githubRepo.branch}?recursive=1`;
const rawBaseUrl = `https://raw.githubusercontent.com/${githubRepo.owner}/${githubRepo.repo}/${githubRepo.branch}/`;

export default async function handleRpcRequest(req) {
  const { method, id, params } = req;

  if (method === "initialize") {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        protocolVersion: "2024-11-05",
        capabilities: {
          resources: { listChanged: true }
        },
        serverInfo: {
          name: "GitHub Repo Server",
          version: "0.1.0"
        }
      }
    };
  }

  if (method === "resources/list") {
    const res = await fetch(githubApiUrl);
    const data = await res.json();

    const files = (data.tree || []).filter(
      (f) => f.type === 'blob' && supportedExtensions.includes(getExt(f.path))
    );

    const resources = files.map((f) => ({
      uri: `github://${githubRepo.owner}/${githubRepo.repo}/${f.path}`,
      name: f.path
    }));

    return {
      jsonrpc: "2.0",
      id,
      result: resources
    };
  }

  if (method === "resources/fetch") {
    const uri = params.uri;
    const path = uri.replace(`github://${githubRepo.owner}/${githubRepo.repo}/`, '');
    const rawUrl = `${rawBaseUrl}${path}`;
    const res = await fetch(rawUrl);
    const content = await res.text();

    return {
      jsonrpc: "2.0",
      id,
      result: {
        uri,
        mimeType: "text/plain",
        content
      }
    };
  }

  return {
    jsonrpc: "2.0",
    id,
    error: {
      code: -32601,
      message: `Method not found: ${method}`
    }
  };
}

function getExt(filePath) {
  return '.' + filePath.split('.').pop();
}
