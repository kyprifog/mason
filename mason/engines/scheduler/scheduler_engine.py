from mason.engines.engine import Engine


class SchedulerEngine(Engine):

    def __init__(self, config: dict):
        super().__init__("scheduler", config)
        self.client = self.get_client()

    def get_client(self):
        client = self.validate()
        from mason.clients.engines.valid_client import ValidClient
        
        if isinstance(client, ValidClient):
            if client.client_name == "glue":
                from mason.clients.glue.scheduler import GlueSchedulerClient
                return GlueSchedulerClient(client.config)
            else:
                from mason.clients.engines.invalid_client import InvalidClient
                return InvalidClient(f"Client type not supported: {client.client_name}")
        else:
            return client

