from pydantic_xml import BaseXmlModel, attr, element
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

"""
Преообразую XML в модель Pydantic.
"""

def _replaceComma(s: str) -> str:
    return s.replace(',', '.')

MyFloat = Annotated[float, BeforeValidator(_replaceComma)] # Использование float с точкой вместо запятой

class Valute(BaseXmlModel):
    ID: str = attr()
    NumCode: int = element()
    CharCode: str = element()
    Nominal: int = element()
    Name: str = element()
    Value: MyFloat = element() #
    VunitRate: MyFloat = element() #

class ValCurs(BaseXmlModel):
    Date: str = attr()
    name: str = attr()
    Valutes: list[Valute] = element(tag='Valute', default=[])
    