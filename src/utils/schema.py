from dataclasses import dataclass
from typing import Any


@dataclass
class ModelResult:
    model: str
    response: str
    tool_calls: list[dict[str, Any]]
    prompt_tokens: int
    reasoning_tokens: int
    total_tokens: int
