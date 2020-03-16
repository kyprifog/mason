from parameters import Parameters
from configurations import Config
from util.environment import MasonEnvironment
from typing import Optional
from operators import operators as Operators
from typing import List

def get(namespace: str, command: str, config: Optional[Config] = None, *args, **kwargs) :
    if not config:
        env = MasonEnvironment()
        config= Config(env)

    param_list: List[str] = []
    for k,v in kwargs.items():
        param_list.append(f"{k}:{v}")

    parameters = ",".join(param_list)
    params = Parameters(parameters)
    response = Operators.run(config, params, namespace, command)

    return response.formatted(), response.status_code