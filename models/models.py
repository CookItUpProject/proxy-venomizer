from multiprocessing import Manager
from http.server import SimpleHTTPRequestHandler

import json
import requests

class CustomProxy(SimpleHTTPRequestHandler):
    """
    CustomProxy extends SimpleHTTPRequestHandler to create a proxy server.

    This proxy server captures and logs GET requests, sends them to the
    specified URL, and logs the responses for testing purposes.
    """

    # Shared list to store captured requests and responses
    petitions = Manager().list()

    def log_message(self, format, *args):
        """
        Suppress the default log messages of the base class.

        Params:
        - format (str): Log message format.
        - *args: Variable number of arguments.
        """

        pass

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_PUT(self):
        self.handle_request('PUT')

    def do_PATCH(self):
        self.handle_request('PATCH')

    def do_DELETE(self):
        self.handle_request('DELETE')

    def do_HEAD(self):
        self.handle_request('HEAD')

    def do_OPTIONS(self):
        self.handle_request('OPTIONS')

    def handle_request(self, method):
        """
        Handle incoming requests for GET, POST, PUT, PATCH, DELETE, HEAD, and OPTIONS.

        This method captures the request, sends it to the specified URL,
        logs relevant information for testing, and sends the response back to the client.

        Params:
        - method (str): HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, or OPTIONS).
        """

        # Extract URL from the request path
        url = self.path[1:]

        # Reading the request body, if any
        content_length = int(self.headers.get('Content-Length', 0))
        request_body = self.rfile.read(content_length)

        try:
            # Sending the request and capturing the response
            response = getattr(requests, method.lower())(url, data=request_body)
            self.handle_response(url, method, request_body, response)

        except Exception as e:
            # Handle exceptions and send a 500 status response
            self.send_response(500)
            self.end_headers()

    def handle_response(self, url, method, request_body, response):
        """
        Common method to handle the response for various HTTP methods.

        Params:
        - url (str): URL of the request.
        - method (str): HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, or OPTIONS).
        - request_body (bytes): Request body.
        - response: Response object from the requests library.
        """

        self.send_response(response.status_code)

        # Copy headers to the response
        for key, value in response.headers.items():
            self.send_header(key, value)

        self.end_headers()

        # Testing the response and logging relevant information
        CustomProxy.petitions.append({
            "name": f"{method} request returns {response.status_code}",
            "type": "http",
            "method": method,
            "url": url,
            "assertions": [
                f"result.statuscode ShouldEqual {response.status_code}",
            ],
            "json_request": json.loads(request_body.decode('utf-8')) if request_body else {},
            "json_response": json.loads(response.text) if response.text else {}
        })

        # Sending the response body in chunks
        for chunk in response.iter_content(chunk_size=1024):
            self.wfile.write(chunk)