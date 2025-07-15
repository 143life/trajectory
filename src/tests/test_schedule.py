import unittest
from datetime import (
    date,
    time,
)

from src.models.day import Day
from src.models.timeslot import Timeslot
from src.services.schedule import ScheduleService


class TestScheduleService(unittest.TestCase):
    def setUp(self):
        days_data = [
            {"id": 1, "date": "2025-02-15", "start": "09:00", "end": "21:00"},
            {"id": 2, "date": "2025-02-16", "start": "08:00", "end": "22:00"},
            {"id": 3, "date": "2025-02-17", "start": "09:00", "end": "18:00"},
            {"id": 4, "date": "2025-02-18", "start": "10:00", "end": "18:00"},
            {"id": 5, "date": "2025-02-19", "start": "09:00", "end": "18:00"},
            {"id": 6, "date": "2025-02-20", "start": "09:00", "end": "18:00"},
            {"id": 7, "date": "2025-02-21", "start": "09:00", "end": "18:00"},
        ]
        days = [Day(**day) for day in days_data]

        timeslots_data = [
            {"id": 1, "day_id": 1, "start": "17:30", "end": "20:00"},
            {"id": 2, "day_id": 1, "start": "09:00", "end": "12:00"},
            {"id": 3, "day_id": 2, "start": "14:30", "end": "18:00"},
            {"id": 4, "day_id": 2, "start": "09:30", "end": "11:00"},
            {"id": 5, "day_id": 3, "start": "12:30", "end": "18:00"},
            {"id": 6, "day_id": 4, "start": "10:00", "end": "11:00"},
            {"id": 7, "day_id": 4, "start": "11:30", "end": "14:00"},
            {"id": 8, "day_id": 4, "start": "14:00", "end": "16:00"},
            {"id": 9, "day_id": 4, "start": "17:00", "end": "18:00"},
            {"id": 10, "day_id": 7, "start": "09:00", "end": "18:00"},
        ]
        timeslots = [Timeslot(**timeslot) for timeslot in timeslots_data]

        self.schedule_service = ScheduleService(days, timeslots)

    def test_get_day_busy_slots_when_free_day(self):
        self.assertEqual(
            self.schedule_service.get_day_busy_slots(
                date.fromisoformat("2025-02-20"),
            ),
            [],
        )

    def test_get_day_busy_slots_when_busy_day(self):
        self.assertEqual(
            self.schedule_service.get_day_busy_slots(
                date.fromisoformat("2025-02-21"),
            ),
            [(time.fromisoformat("09:00"), time.fromisoformat("18:00"))],
        )

    def test_get_day_busy_slots_when_busy_slots(self):
        self.assertEqual(
            self.schedule_service.get_day_busy_slots(
                date.fromisoformat("2025-02-16"),
            ),
            [
                (time.fromisoformat("09:30"), time.fromisoformat("11:00")),
                (time.fromisoformat("14:30"), time.fromisoformat("18:00")),
            ],
        )

    def test_get_day_free_slots_when_day_not_in_db(self):
        self.assertEqual(
            self.schedule_service.get_day_free_slots(
                date.fromisoformat("2025-03-22"),
            ),
            [],
        )

    def test_get_day_free_slots(self):
        self.assertEqual(
            self.schedule_service.get_day_free_slots(
                date.fromisoformat("2025-02-15"),
            ),
            [
                (time.fromisoformat("12:00"), time.fromisoformat("17:30")),
                (time.fromisoformat("20:00"), time.fromisoformat("21:00")),
            ],
        )

    def test_is_available(self):
        self.assertEqual(
            self.schedule_service.is_available(
                date.fromisoformat("2025-02-15"),
                time.fromisoformat("20:30"),
                time.fromisoformat("21:00"),
            ),
            True,
        )

    def test_find_free_slot(self):
        self.assertEqual(
            self.schedule_service.find_free_slot(hours=1, minutes=35),
            (
                date.fromisoformat("2025-02-15"),
                time.fromisoformat("12:00"),
                time.fromisoformat("13:35"),
            ),
        )


unittest.main()
