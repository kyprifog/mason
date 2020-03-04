
import datetime
import json
from pygments import highlight, lexers, formatters # type: ignore

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def to_json(d: dict):
    dump = json.dumps(
        d,
        sort_keys=False,
        indent=1,
        default=default
    )
    return dump

def print_json(d: dict):
    formatted_json = to_json(d)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    return print(colorful_json)

def print_json_1level(d: dict):
    out = {}
    for key, value in d.items():
        out[key] = str(value)
    print_json(out)
