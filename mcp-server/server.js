// server.js
import http from 'http';
import createRpcHandler from './rpc_handler.js';

let githubOptions = null;

const handleHttpRequest = async (req, res) => {
  if (req.method === 'POST' && req.url === '/rpc') {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
    });
    req.on('end', async () => {
      try {
        const rpcRequest = JSON.parse(body);

        if (rpcRequest.method === 'initialize') {
          const params = rpcRequest.params || {};
          const { owner, repo, branch = 'main' } = params;
          if (!owner || !repo) {
            const errorResponse = {
              jsonrpc: "2.0",
              id: rpcRequest.id || null,
              error: {
                code: -32602,
                message: "Missing required initialize parameters: owner and repo"
              }
            };
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(errorResponse));
            return;
          }
          githubOptions = { owner, repo, branch };
          const response = {
            jsonrpc: "2.0",
            id: rpcRequest.id,
            result: {
              message: `Configured GitHub repo: ${owner}/${repo}@${branch}`
            }
          };
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(response));
          return;
        }

        if (!githubOptions) {
          const errorResponse = {
            jsonrpc: "2.0",
            id: rpcRequest.id || null,
            error: {
              code: -32000,
              message: "Server not initialized. Call initialize with owner and repo first."
            }
          };
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(errorResponse));
          return;
        }

        const handler = createRpcHandler(githubOptions);
        const response = await handler(rpcRequest);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(response));
      } catch (err) {
        const errorResponse = {
          jsonrpc: "2.0",
          id: null,
          error: {
            code: -32603,
            message: err.message
          }
        };
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(errorResponse));
      }
    });
  } else {
    res.writeHead(404);
    res.end();
  }
};

const PORT = 4000;
const server = http.createServer(handleHttpRequest);

server.listen(PORT, () => {
  console.log(`🚀 MCP HTTP server listening on http://localhost:${PORT}`);
});

