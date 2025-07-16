from datetime import (
    date,
    datetime,
    time,
    timedelta,
)

from src.models.day import Day
from src.models.timeslot import Timeslot


class ScheduleService:
    """Service for managing and querying schedule data."""

    def __init__(self, days: list[Day], timeslots: list[Timeslot]):
        self.days = {day.date: day for day in days}
        self.timeslots = list(timeslots)

    def get_day_busy_slots(self, target_date: date) -> list[tuple[time, time]]:
        """Find all busy time slots for a given date."""
        if not isinstance(target_date, date):
            raise TypeError("target_date должен быть объектом datetime.date")

        result = []
        if target_date in self.days:
            day_id = self.days[target_date].id
            for timeslot in self.timeslots:
                if timeslot.day_id == day_id:
                    result.append((timeslot.start, timeslot.end))
        result.sort(key=lambda x: x[0])
        return result

    def get_day_free_slots(self, target_date: date) -> list[tuple[time, time]]:
        """Find all free time slots for a given date."""
        if not isinstance(target_date, date):
            raise TypeError("target_date должен быть объектом datetime.date")

        result = []
        if target_date not in self.days:
            return result

        busy_slots = self.get_day_busy_slots(target_date=target_date)
        if not busy_slots:
            return [(self.days[target_date].start, self.days[target_date].end)]

        busy_slots.sort(key=lambda x: x[0])
        start_time = self.days[target_date].start

        # find free slots between busy (and start)
        for i in range(len(busy_slots)):
            if start_time != busy_slots[i][0]:
                result.append((start_time, busy_slots[i][0]))
            start_time = busy_slots[i][1]

        # check last busy end and end of the day
        if start_time != self.days[target_date].end:
            result.append((start_time, self.days[target_date].end))

        return result

    def is_available(self, target_date: date, start: time, end: time) -> bool:
        """Check if a time interval is available on a given date."""
        if start >= end:
            raise ValueError("start должен быть меньше end")
        if not isinstance(target_date, date):
            raise TypeError("target_date должен быть объектом datetime.date")
        if not isinstance(start, time) or not isinstance(end, time):
            raise TypeError("start и end должны быть объектами datetime.time")

        free_slots = self.get_day_free_slots(target_date=target_date)

        if not free_slots:
            return False

        for free_slot in free_slots:
            if start >= free_slot[0] and end <= free_slot[1]:
                return True
        return False

    def find_free_slot(
        self,
        hours: int,
        minutes: int,
    ) -> tuple[date, time, time] | None:
        """Find a free time slot for a request of given duration."""
        if hours < 0 or minutes < 0 or hours == 0 and minutes == 0:
            raise ValueError("время не может быть отрицательным или равно 0")
        requested_time = timedelta(hours=hours, minutes=minutes)
        for day in sorted(self.days):
            free_slots = self.get_day_free_slots(target_date=day)
            if not free_slots:
                continue
            for free_slot in free_slots:
                start_datetime = datetime.combine(date.min, free_slot[0])
                end_datetime = start_datetime + requested_time
                calculated_end = end_datetime.time()
                if (
                    calculated_end <= free_slot[1]
                    and end_datetime.date() == date.min
                ):
                    return (day, free_slot[0], calculated_end)
        return None
