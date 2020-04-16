from typing import Sequence

from tabulator import FormatError # type: ignore

from clients.response import Response
from engines.metastore.models.schemas.metastore_schema import MetastoreSchema, SchemaElement, emptySchema

from tableschema import Table # type: ignore

class TextElement(SchemaElement):

    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
        super().__init__(name, type)

class TextSchema(MetastoreSchema):

    def __init__(self, columns: Sequence[TextElement], type: str):
        self.columns = columns
        if type == "none":
            self.type = 'text'
        else:
            self.type = 'text' + "-" + type


def from_file(file_name: str, type: str, read_headers: bool, response: Response) -> TextSchema:
    table = Table(file_name, headers=read_headers)
    try:
        table.infer()
        fields = table.schema.descriptor.get('fields')
        columns = list(map(lambda f: TextElement(f.get('name'), f.get('type')), fields))

        errors = table.schema.errors
        for e in errors:
            response.add_error(e)

        return TextSchema(columns, type)
    except FormatError as e:
        response.add_warning(f'File type not supported for file {file_name}')
        return emptySchema()




