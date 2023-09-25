const fs = require('fs');
const net = require('net');

// Load config from external JSON file
const loadConfig = (filePath) => {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
};

// Load and use the configuration
const config = loadConfig('./config.json'); // Update this path
const HOST = config.host;
const PORT = config.port;

const client = new net.Socket();
client.connect(PORT, HOST, function() {
  console.log('Connected');
  const request = {
    method: "floor",
    params: [5.7],
    param_types: ["double"],
    id: 1
  };
  client.write(JSON.stringify(request));
});

client.on('data', function(data) {
  console.log('Received:', data.toString());
  client.destroy();
});

client.on('close', function() {
  console.log('Connection closed');
});
