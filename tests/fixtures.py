import pytest

from src.main import CounterLogs


@pytest.fixture
def fixture_level():
    return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

@pytest.fixture
def fixture_flag():
    return "--handler"

@pytest.fixture
def fixture_file(tmp_path):
    log_file = tmp_path / "test_api.log"
    logs = """\
    2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]
    2025-03-28 12:05:13,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.97]
    2025-03-28 12:02:07,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.35]
    2025-03-27 12:47:00,000 ERROR django.request: Internal Server Error: /api/v1/reviews/ [192.168.1.47] - ValueError: Invalid input data
    2025-03-28 12:02:07,000 WARNING django.request: GET /api/v1/reviews/ 300 OK [192.168.1.35]
    2025-03-27 12:47:00,000 CRITICAL django.request: Internal Server Error: /api/v1/reviews/1 [192.168.1.47] - ValueError: Invalid input data
    """
    log_file.write_text(logs.strip())
    return [str(log_file)]

@pytest.fixture
def fixture_files(tmp_path):
    log_file_1 = tmp_path / "test_api_1.log"
    logs1 = """\
    2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]
    2025-03-28 12:05:13,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.97]
    2025-03-28 12:02:07,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.35]
    """

    log_file_2 = tmp_path / "test_api_2.log"
    logs2 = """\
    2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]
    2025-03-28 12:05:13,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.97]
    2025-03-28 12:02:07,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.35]
    2025-03-27 12:47:00,000 ERROR django.request: Internal Server Error: /api/v1/reviews/ [192.168.1.47] - ValueError: Invalid input data
    2025-03-28 12:02:07,000 WARNING django.request: GET /api/v1/reviews/ 300 OK [192.168.1.35]
    2025-03-27 12:47:00,000 CRITICAL django.request: Internal Server Error: /api/v1/reviews/1 [192.168.1.47] - ValueError: Invalid input data
    """
    log_file_1.write_text(logs1)
    log_file_2.write_text(logs2)
    return [str(log_file_1), str(log_file_2)]

@pytest.fixture
def fixture_counter_log_1(fixture_file, fixture_flag, fixture_level):
    counter_log: CounterLogs = CounterLogs(logs_level=fixture_level,
                                           flag=fixture_flag,
                                           path_files=fixture_file)
    yield counter_log

@pytest.fixture
def fixture_counter_log_2(fixture_files, fixture_flag, fixture_level):
    counter_log: CounterLogs = CounterLogs(logs_level=fixture_level,
                                           flag=fixture_flag,
                                           path_files=fixture_files)
    yield counter_log


