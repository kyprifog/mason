
from mason.clients.base import Client
from mason.clients.response import Response


class InvalidClient(Client):

    def __init__(self, reason: str):
        self.reason = reason
        self.client = NullClient()
        
    def __getattr__(self, name):
        def _missing(response: Response, *args, **kwargs) -> Response:
            response.add_error(f"Invalid Client: {self.reason}")
            return response
        return _missing


class NullClient:
    def name(self):
        return "invalid"
    
