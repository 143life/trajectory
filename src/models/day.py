from datetime import (
    date,
    time,
)

from pydantic import BaseModel


class Day(BaseModel):
    id: int  # noqa
    date: date
    start: time
    end: time
