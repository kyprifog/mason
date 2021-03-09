import re
from typing import List, Optional

class Path:

    def __init__(self, path_str: str, protocal: str = "file"):
        self.protocal = protocal
        self.path_str = path_str
        
    def clean_path_str(self) -> str:
        return re.sub(r'(?<=[^:])\/\/', '/', self.full_path())

    def full_path(self) -> str:
        if self.protocal != "file":
            return "://".join([self.protocal, self.path_str])
        else:
            return self.path_str
        

def construct(parts: List[str], protocal: Optional[str] = None) -> Path:
    strp = list(map(lambda p: p.strip("/"), parts))
    return Path("/".join(strp), protocal or "file")
    