from pandas import DataFrame

from mason.clients.responsable import Responsable
from mason.clients.response import Response
from mason.engines.metastore.models.schemas.schema import Schema

class TableSummary(Responsable):
    
    def __init__(self):
        pass
    
    def to_response(self, response: Response):
        response.add_data()
        return response
    
def from_df(dataframe: DataFrame) -> TableSummary:
    return TableSummary()

class NullCounts:
    
    def __init__(self, schema: Schema):
        self.schema = schema