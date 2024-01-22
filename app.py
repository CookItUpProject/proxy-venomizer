from multiprocessing import Manager
from socketserver import ForkingTCPServer

from models.models import CustomProxy
from handlers.venom import write_tests

def run(port: int = 9797):
    """
    Run the proxy server on the specified port.

    Params:
    - port (int): The port number on which the proxy server will listen. Default is set to 9797.
    """
    
    try:
        # Display information about the server startup
        print(f"[INFO] Proxy server starting on port {port}")

        # Create a Forking TCP server with the custom proxy handler
        httpd = ForkingTCPServer(('', port), CustomProxy)
        httpd.serve_forever()

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt to gracefully shut down the server
        httpd.server_close()
        print(f"[INFO] Proxy server stopped")

    finally:
        # Perform cleanup and write tests after server shutdown
        print(f"[INFO] Writing tests")
        write_tests(CustomProxy.petitions)

if __name__ == "__main__":
    # Run the server
    run()
