const express = require('express');
const cors = require('cors');

const app = express();

// Enable all CORS requests
app.use(cors());

// REST API routes
app.get('/api/endpoint', (req, res) => {
  // Handle GET request for /api/endpoint
  // Implement your logic here
});

app.post('/api/endpoint', (req, res) => {
  // Handle POST request for /api/endpoint
  // Implement your logic here
});

// ... Rest of your server code

const port = process.env.PORT || 5000; // Use the PORT environment variable if available, or fallback to a default port (e.g., 5000)

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});