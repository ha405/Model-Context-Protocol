FROM node:18-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy server files (from current directory)
COPY . .

# Expose the server port
EXPOSE 4000

# Start the server
CMD [ "node", "server.js" ]