#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('web-service')

# Constants
STATUS_FILE = '/usr/src/app/status.json'
DEFAULT_STATUS = {
    "status": "unknown",
    "message": "Waiting for config monitor to provide status",
    "timestamp": time.time()
}
SERVER_PORT = 8080

class StatusHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def get_status(self):
        """Read status from file, return default if not available"""
        try:
            if Path(STATUS_FILE).exists():
                with open(STATUS_FILE, 'r') as f:
                    status_data = json.load(f)
                    # Check if data is stale (older than 1 minute)
                    if time.time() - status_data.get('timestamp', 0) > 60:
                        logger.warning("Status file data is stale")
                        status_data['message'] += " (STALE DATA)"
                return status_data
            else:
                logger.warning(f"Status file not found at {STATUS_FILE}")
                return DEFAULT_STATUS
        except Exception as e:
            logger.error(f"Error reading status file: {str(e)}")
            return DEFAULT_STATUS

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/health':
            # Health endpoint returns JSON
            self._set_headers('application/json')
            status_data = self.get_status()
            self.wfile.write(json.dumps(status_data).encode())
            return

        # Default path returns HTML with happy/sad face
        self._set_headers()
        status_data = self.get_status()

        # Get status emoji and color
        if status_data['status'] == 'healthy':
            emoji = '🤠'  # Cowboy face!
            color = 'green'
            bg_color = '#e6ffe6'  # Light green
        elif status_data['status'] == 'unknown':
            emoji = '😐'  # Neutral face
            color = 'orange'
            bg_color = '#fff9e6'  # Light yellow
        else:
            emoji = '😢'  # Sad face
            color = 'red'
            bg_color = '#ffe6e6'  # Light red

        # Create the HTML response
        html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Config Status</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: {bg_color};
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .container {{
                    text-align: center;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    background-color: white;
                    max-width: 500px;
                }}
                .status {{
                    font-size: 100px;
                    margin: 20px 0;
                }}
                .message {{
                    color: {color};
                    font-weight: bold;
                    margin-bottom: 20px;
                }}
                .details {{
                    color: #666;
                    font-size: 0.9rem;
                }}
                .refresh {{
                    margin-top: 20px;
                    font-size: 0.8rem;
                    color: #999;
                }}
            </style>
            <script>
                // Auto-refresh every 10 seconds
                setTimeout(function() {{
                    window.location.reload();
                }}, 10000);
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Kubernetes Config Status</h1>
                <div class="status">{emoji}</div>
                <div class="message">Status: {status_data['status'].upper()}</div>
                <div class="details">{status_data['message']}</div>
            </div>
        </body>
        </html>
        '''

        self.wfile.write(html.encode())

def run_server():
    server_address = ('', SERVER_PORT)
    httpd = HTTPServer(server_address, StatusHandler)
    logger.info(f'Starting web server on port {SERVER_PORT}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('Shutting down web server...')
        httpd.server_close()

if __name__ == '__main__':
    run_server()