// server.js
import http from 'http';
import  handleRpcRequest  from './rpc_handler.js';

const PORT = 4000;

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/rpc') {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
    });
    req.on('end', async () => {
      try {
        const request = JSON.parse(body);
        const response = await handleRpcRequest(request);
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
});

server.listen(PORT, () => {
  console.log(`MCP HTTP server listening on port ${PORT}`);
});
