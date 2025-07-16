import unittest
from datetime import (
	date,
	time,
)

from src.models.day import Day
from src.models.timeslot import Timeslot
from src.services.schedule import ScheduleService


class TestScheduleService(unittest.TestCase):
	"""Test cases for ScheduleService functionality."""

	def setUp(self):
		"""Set up test data with days and timeslots."""
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
		"""Test get_day_busy_slots when day has no busy slots."""
		self.assertEqual(
			self.schedule_service.get_day_busy_slots(
				target_date=date.fromisoformat("2025-02-20"),
			),
			[],
		)

	def test_get_day_busy_slots_when_busy_day(self):
		"""Test get_day_busy_slots when day is fully busy."""
		self.assertEqual(
			self.schedule_service.get_day_busy_slots(
				target_date=date.fromisoformat("2025-02-21"),
			),
			[(time.fromisoformat("09:00"), time.fromisoformat("18:00"))],
		)

	def test_get_day_busy_slots_when_busy_slots(self):
		"""Test get_day_busy_slots when day has multiple busy slots."""
		self.assertEqual(
			self.schedule_service.get_day_busy_slots(
				target_date=date.fromisoformat("2025-02-16"),
			),
			[
				(time.fromisoformat("09:30"), time.fromisoformat("11:00")),
				(time.fromisoformat("14:30"), time.fromisoformat("18:00")),
			],
		)

	def test_get_day_free_slots_when_day_not_in_db(self):
		"""Test get_day_free_slots when date is not in schedule."""
		self.assertEqual(
			self.schedule_service.get_day_free_slots(
				target_date=date.fromisoformat("2025-03-22"),
			),
			[],
		)

	def test_get_day_free_slots(self):
		"""Test get_day_free_slots with normal busy slots."""
		self.assertEqual(
			self.schedule_service.get_day_free_slots(
				target_date=date.fromisoformat("2025-02-15"),
			),
			[
				(time.fromisoformat("12:00"), time.fromisoformat("17:30")),
				(time.fromisoformat("20:00"), time.fromisoformat("21:00")),
			],
		)
	
	def test_get_day_free_slots_when_busy_slots(self):
		"""Test get_day_free_slots when day is fully busy."""
		self.assertEqual(
			self.schedule_service.get_day_free_slots(
				target_date=date.fromisoformat("2025-02-21"),
			),
			[]
		)
	
	def test_get_day_free_slots_when_free_day(self):
		"""Test get_day_free_slots when day has no busy slots."""
		self.assertEqual(
			self.schedule_service.get_day_free_slots(
				target_date=date.fromisoformat("2025-02-20"),
			),
			[(time.fromisoformat("09:00"), time.fromisoformat("18:00"))],
		)

	def test_is_available(self):
		"""Test is_available with available time slot."""
		self.assertEqual(
			self.schedule_service.is_available(
				target_date=date.fromisoformat("2025-02-15"),
				start=time.fromisoformat("20:30"),
				end=time.fromisoformat("21:00"),
			),
			True,
		)
	
	def test_is_available_when_start_time_crossed_busy_slots(self):
		"""Test is_available when start time overlaps with busy slot."""
		self.assertEqual(
			self.schedule_service.is_available(
				target_date=date.fromisoformat("2025-02-15"),
				start=time.fromisoformat("11:00"),
				end=time.fromisoformat("13:00"),
			),
			False,
		)

	def test_is_available_when_end_time_crossed_busy_slots(self):
		"""Test is_available when end time overlaps with busy slot."""
		self.assertEqual(
			self.schedule_service.is_available(
				target_date=date.fromisoformat("2025-02-15"),
				start=time.fromisoformat("13:00"),
				end=time.fromisoformat("18:00"),
			),
			False,
		)

	def test_is_available_when_time_fully_match_busy_slot(self):
		"""Test is_available when time exactly matches busy slot."""
		self.assertEqual(
			self.schedule_service.is_available(
				target_date=date.fromisoformat("2025-02-15"),
				start=time.fromisoformat("17:30"),
				end=time.fromisoformat("20:00"),
			),
			False,
		)
	
	def test_is_available_when_time_fully_match_free_slot(self):
		"""Test is_available when time exactly matches free slot."""
		self.assertEqual(
			self.schedule_service.is_available(
				target_date=date.fromisoformat("2025-02-15"),
				start=time.fromisoformat("20:00"),
				end=time.fromisoformat("21:00"),
			),
			True,
		)

	def test_find_free_slot(self):
		"""Test find_free_slot with valid duration."""
		self.assertEqual(
			self.schedule_service.find_free_slot(hours=1, minutes=35),
			(
				date.fromisoformat("2025-02-15"),
				time.fromisoformat("12:00"),
				time.fromisoformat("13:35"),
			),
		)
	
	def test_find_free_slot_24_plus_hours(self):
		"""Test find_free_slot with duration longer than 24 hours."""
		self.assertEqual(
			self.schedule_service.find_free_slot(hours=24, minutes=0),
			None,
		)
	
	def test_find_free_slot_when_not_enough_space_in_slots(self):
		"""Test find_free_slot when no slot can accommodate the request."""
		self.assertEqual(
			self.schedule_service.find_free_slot(hours=10, minutes=35),
			None,
		)

	# error handling tests
	def test_is_available_invalid_time_range(self):
		"""Test when start >= end."""
		with self.assertRaises(ValueError):
			self.schedule_service.is_available(
				target_date=date.fromisoformat("2025-02-15"),
				start=time.fromisoformat("21:00"),
				end=time.fromisoformat("20:00"),
			)

	def test_is_available_equal_start_end(self):
		"""Test when start == end."""
		with self.assertRaises(ValueError):
			self.schedule_service.is_available(
				target_date=date.fromisoformat("2025-02-15"),
				start=time.fromisoformat("20:00"),
				end=time.fromisoformat("20:00"),
			)

	def test_find_free_slot_negative_hours(self):
		"""Test with negative hours."""
		with self.assertRaises(ValueError):
			self.schedule_service.find_free_slot(hours=-1, minutes=0)

	def test_find_free_slot_negative_minutes(self):
		"""Test with negative minutes."""
		with self.assertRaises(ValueError):
			self.schedule_service.find_free_slot(hours=1, minutes=-30)

	def test_find_free_slot_both_negative(self):
		"""Test with both negative hours and minutes."""
		with self.assertRaises(ValueError):
			self.schedule_service.find_free_slot(hours=-2, minutes=-15)

	def test_find_free_slot_zero_duration(self):
		"""Test with zero duration."""
		with self.assertRaises(ValueError):
			self.schedule_service.find_free_slot(hours=0, minutes=0)

	def test_is_available_wrong_date_type(self):
		"""Test with wrong date type: string instead of date."""
		with self.assertRaises(TypeError):
			self.schedule_service.is_available(
				target_date="2025-02-15",
				start=time.fromisoformat("20:30"),
				end=time.fromisoformat("21:00"),
			)

	def test_get_day_busy_slots_wrong_date_type(self):
		"""Test get_day_busy_slots with wrong date type."""
		with self.assertRaises(TypeError):
			self.schedule_service.get_day_busy_slots(
				target_date="2025-02-15"
			)

	def test_get_day_free_slots_wrong_date_type(self):
		"""Test get_day_free_slots with wrong date type."""
		with self.assertRaises(TypeError):
			self.schedule_service.get_day_free_slots(
				target_date="2025-02-15"
			)


unittest.main()
