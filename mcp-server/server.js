import readline from 'readline';
import  handleRpcRequest  from './rpc_handler.js';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', async(line) => {
    try {
    const request = JSON.parse(line);
    const response = await handleRpcRequest(request);
    process.stdout.write(JSON.stringify(response) + "\n");
  } catch (err) {
    const errorResponse = {
      jsonrpc: "2.0",
      id: null,
      error: {
        code: -32603,
        message: err.message
      }
    };
    process.stdout.write(JSON.stringify(errorResponse) + "\n");
  }
})

