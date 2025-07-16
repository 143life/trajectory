from datetime import (
    date,
    time,
)

from pydantic import BaseModel


class Day(BaseModel):
    """Model representing a working day with start and end times."""

    id: int  # noqa
    date: date
    start: time
    end: time
