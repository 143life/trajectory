from datetime import time

from pydantic import BaseModel


class Timeslot(BaseModel):
    id: int  # noqa
    day_id: int
    start: time
    end: time
