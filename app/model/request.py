from typing import List

from pydantic import BaseModel


class LogRequest(BaseModel):
    services: List[str]
    level: str
    queries: List[str]
    limit: int | None = None
