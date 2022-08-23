#!/usr/bin/env python

import json
from pathlib import Path

from pydantic import BaseModel

from trial_balloon.models import root_models

ROOT = Path(__file__).parent.parent
SCHEMAS_PATH = ROOT / 'trial_balloon' / 'schemas'


def dump_schema(name: str, root_model: BaseModel, folder: Path = SCHEMAS_PATH):
    with open(folder / f'{name}.json', 'w') as fp:
        json.dump(root_model.schema(), fp, indent=2)


def main():
    for name, model in root_models.items():
        dump_schema(name, model)


if __name__ == '__main__':
    main()
