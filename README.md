# Trajectory - Schedule Management Service

A service for working with schedules that provides functionality for finding busy and free time slots, checking time availability, and finding suitable intervals for requests.

## 🚀 Features

- **Find busy slots** for a specified date
- **Find free slots** between busy intervals
- **Check availability** of a specific time interval
- **Find free time** for a request of given duration
- **API integration** for retrieving schedule data

## 📋 Requirements

- Python 3.9+
- Poetry (for dependency management)

## 🛠 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/143life/trajectory.git
cd trajectory
```

2. **Install dependencies:**
```bash
poetry install
```

## 🧪 Running Tests

### Run all tests:
```bash
poetry run python -m src.tests.test_schedule
```

### Run with verbose output:
```bash
poetry run python -m src.tests.test_schedule -v
```

### Run specific test:
```bash
poetry run python -m src.tests.test_schedule TestScheduleService.test_is_available
```

## 🔧 Main Methods

### `ScheduleService`

- **`get_day_busy_slots(target_date)`** - find busy slots for a date
- **`get_day_free_slots(target_date)`** - find free slots for a date
- **`is_available(target_date, start, end)`** - check interval availability
- **`find_free_slot(hours, minutes)`** - find free time for a request

### `APIClient`

- **`fetch_schedule()`** - get schedule data from API

## 🧪 Testing

The project includes comprehensive unit tests covering:

- ✅ Finding busy slots (empty day, busy day, partially busy)
- ✅ Finding free slots (various scenarios)
- ✅ Checking availability (overlaps, exact matches)
- ✅ Finding free time (edge cases, large intervals)
- ✅ Error handling and invalid data

## 🛡 Error Handling

The service includes input data validation:

- Parameter type checking
- Time interval validation (start < end)
- Negative value checking
- API error handling

## 🚀 Development

### Pre-commit hooks:
```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```
