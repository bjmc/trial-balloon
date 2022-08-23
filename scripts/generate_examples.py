#!/usr/bin/env python

from pathlib import Path

from pydantic import BaseModel

from trial_balloon.fixtures import FIXTURES

ROOT = Path(__file__).parent.parent
EXAMPLES_PATH = ROOT / 'trial_balloon' / 'examples'


def dump_examples(name: str, record: BaseModel, folder: Path = EXAMPLES_PATH):
    with open(folder / f'{name}.json', 'w') as fp:
        fp.write(record.json(indent=2))


def main():
    for name, record in FIXTURES:
        dump_examples(name, record)


if __name__ == '__main__':
    main()
