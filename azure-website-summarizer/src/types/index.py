from typing import TypedDict, Union

class InputData(TypedDict):
    content: Union[str, None]
    url: Union[str, None]

class SummaryResult(TypedDict):
    summary: str
    source: Union[str, None]