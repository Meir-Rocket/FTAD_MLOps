import ast
import os
from typing import Dict, Any

import yaml

CONFIG_ENV_VAR: str = 'ML_OPS_CONFIG'


def load_env_vars(cfg: Dict[str, Any]) -> None:
    for key in cfg:
        if key in os.environ:
            cfg[key] = ast.literal_eval(os.getenv(key))


def load_config() -> Dict[str, Any]:
    with open('configuration/default.yaml', 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    working_cfg_path = os.getenv(CONFIG_ENV_VAR, None)
    if working_cfg_path is not None:
        with open(ast.literal_eval(working_cfg_path), 'r') as f:
            cfg.update(yaml.load(f, Loader=yaml.FullLoader))
    load_env_vars(cfg)
    return cfg
