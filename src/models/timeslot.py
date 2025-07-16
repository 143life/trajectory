from datetime import time

from pydantic import BaseModel


class Timeslot(BaseModel):
	"""Model representing a time slot within a working day."""

	id: int  # noqa
	day_id: int
	start: time
	end: time
