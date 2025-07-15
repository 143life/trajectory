from datetime import (
    date,
    datetime,
    time,
    timedelta,
)

from src.models.day import Day
from src.models.timeslot import Timeslot


class ScheduleService:
    def __init__(self, days: list[Day], timeslots: list[Timeslot]):
        self.days = {day.date: day for day in days}
        self.timeslots = list(timeslots)

    # find all busy slots for date
    def get_day_busy_slots(self, date: date) -> list[tuple[time, time]]:
        result = []
        # if date in DB
        if date in self.days:
            day_id = self.days[date].id
            # search timeslots for this day
            for timeslot in self.timeslots:
                if timeslot.day_id == day_id:
                    result.append((timeslot.start, timeslot.end))
        result.sort(key=lambda x: x[0])
        return result

    # find free time for date
    def get_day_free_slots(self, date: date) -> list[tuple[time, time]]:
        result = []
        if date not in self.days:
            return result

        busy_slots = self.get_day_busy_slots(date=date)
        if not busy_slots:
            return [(self.days[date].start, self.days[date].end)]

        busy_slots.sort(key=lambda x: x[0])
        start_time = self.days[date].start

        # find free slots between busy (and start)
        for i in range(len(busy_slots)):
            if start_time != busy_slots[i][0]:
                result.append((start_time, busy_slots[i][0]))
            start_time = busy_slots[i][1]

        # check last busy end and end of the day
        if start_time != self.days[date].end:
            result.append((start_time, self.days[date].end))

        return result

    # is slot available for date
    def is_available(self, date: date, start: time, end: time) -> bool:
        free_slots = self.get_day_free_slots(date=date)

        if not free_slots:
            return False

        for free_slot in free_slots:
            if start >= free_slot[0] and end <= free_slot[1]:
                return True
        return False

    # find free time for request
    def find_free_slot(
        self,
        hours: int,
        minutes: int,
    ) -> tuple[date, time, time] | None:
        requested_time = timedelta(hours=hours, minutes=minutes)
        for day in sorted(self.days):
            free_slots = self.get_day_free_slots(date=day)
            if not free_slots:
                continue
            for free_slot in free_slots:
                calculated_end = (
                    datetime.combine(date.min, free_slot[0]) + requested_time
                ).time()
                if calculated_end <= free_slot[1]:
                    return (day, free_slot[0], calculated_end)
        return None
