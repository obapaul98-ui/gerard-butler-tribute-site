import http.server
import socketserver
import os
import json
from urllib.parse import urlparse
from urllib import request as urllib_request

PORT = 8081
BACKEND_URL = "http://127.0.0.1:3000"

class ThreadingSimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        # Health check proxy
        if path.startswith('/api/'):
            return self._proxy_to_backend('GET')
        
        # If accessing root, serve index.html
        if path == '/':
            self.path = '/index.html' + ('?' + parsed.query if parsed.query else '')
            return super().do_GET()
            
        # If the requested path has no extension and doesn't end with a slash,
        # try adding .html to see if the file exists.
        if path != '/' and '.' not in path:
            possible_html_file = path.lstrip('/') + '.html'
            if os.path.exists(possible_html_file):
                # rewrite the path but keep the query string
                new_path = '/' + possible_html_file
                if parsed.query:
                    new_path += '?' + parsed.query
                self.path = new_path
                
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith('/api/'):
            return self._proxy_to_backend('POST')
        
        self.send_error(404, "Not Found")

    def _proxy_to_backend(self, method):
        """Forward /api/* requests to the Flask backend on port 3000"""
        target_url = BACKEND_URL + self.path
        
        try:
            # Read request body for POST
            body = None
            headers = {}
            if method == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length) if content_length else None
                content_type = self.headers.get('Content-Type', 'application/json')
                headers['Content-Type'] = content_type

            req = urllib_request.Request(
                target_url,
                data=body,
                headers=headers,
                method=method
            )
            
            with urllib_request.urlopen(req) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                self.send_header('Content-Type', resp.getheader('Content-Type', 'application/json'))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp_body)
                
        except Exception as e:
            error_msg = json.dumps({"error": f"Backend unavailable: {str(e)}"})
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_msg.encode())

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

with ThreadingSimpleServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT} with extensionless URLs (Threading Enabled)")
    print(f"API proxy → {BACKEND_URL}")
    httpd.serve_forever()
