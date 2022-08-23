'''
Heavily inspired by:
https://ianwhitestone.work/data-templates-with-pydantic/
'''
from typing import List, NamedTuple

from pydantic import BaseModel


class NamedFixture(NamedTuple):
    name: str
    fixture: BaseModel


class DataTemplate:
    def __init__(self, template: BaseModel):
        self.template = template

    def __repr__(self) -> str:
        return f'DataTemplate({self.template})'

    def __str__(self) -> str:
        return str(self.template)

    @property
    def default(self) -> BaseModel:
        '''Return a single model containing the default values'''
        return self.template.copy()

    def record(self, **kwargs) -> BaseModel:
        '''Generate a new instance from the template with modified properties.'''
        return self.template.parse_obj(dict(self.template.dict(), **kwargs))

    def records(self, records: List[BaseModel]) -> List[BaseModel]:
        '''Generate a list of new instances with modified properties.'''
        return [self.record(**r.dict()) for r in records]
