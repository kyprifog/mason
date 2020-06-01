from mason.clients.athena.metastore import AthenaMetastoreClient
from mason.clients.engines.invalid_client import InvalidClient
from mason.clients.engines.valid_client import ValidClient
from mason.clients.glue.metastore import GlueMetastoreClient
from mason.clients.s3.metastore import S3MetastoreClient
from mason.engines.engine import Engine


class MetastoreEngine(Engine):

    def __init__(self, config: dict):
        super().__init__("metastore", config)
        self.client = self.get_client()

    def get_client(self):
        client = self.validate()
        if isinstance(client, ValidClient):
            if self.client_name == "glue":
                return GlueMetastoreClient(client.config)
            elif self.client_name == "s3":
                return S3MetastoreClient(client.config)
            elif self.client_name == "athena":
                return AthenaMetastoreClient(client.config)
            else:
                return InvalidClient(f"Client type not supported: {client.client_name}")
        else:
            return client

