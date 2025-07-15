from typing import List

from pydantic import BaseModel


class LogRequest(BaseModel):
    service: str
    level: str
    queries: List[str]
    limit: int | None = None
