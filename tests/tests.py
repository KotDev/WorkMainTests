from typing import List
import pytest
from .fixtures import (fixture_counter_log_1,
                      fixture_counter_log_2,
                      fixture_level,
                      fixture_flag,
                      fixture_file,
                      fixture_files)
from src.main import CounterLogs

class TestCounterLog:

    @pytest.mark.asyncio
    def test_initial(self, fixture_counter_log_1, fixture_level, fixture_file, fixture_flag):
        assert fixture_counter_log_1.logs_level == fixture_level
        assert fixture_counter_log_1.flag == fixture_flag
        assert fixture_counter_log_1.path_files == fixture_file
        assert fixture_counter_log_1.total_counter == 0
        assert len(fixture_counter_log_1.report.keys()) == 0

    @pytest.mark.asyncio
    async def test_exists_file(self, fixture_file: List[str], fixture_level: List[str], fixture_flag: str) -> None:
        fixture_file.append("test.log")
        with pytest.raises(ValueError) as exc_info:
            CounterLogs(
                flag=fixture_flag,
                logs_level=fixture_level,
                path_files=fixture_file
            )
        assert "such test.log does not exists in folder logs" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_counter_logs(self, fixture_counter_log_1: CounterLogs, fixture_file: List[str]) -> None:
        await fixture_counter_log_1.counters_log(fixture_file[0])
        assert fixture_counter_log_1.total_counter == 6
        assert fixture_counter_log_1.report["/api/v1/reviews/"]["INFO"] == 3
        assert fixture_counter_log_1.report["/api/v1/reviews/"]["ERROR"] == 1
        assert fixture_counter_log_1.report["/api/v1/reviews/"]["WARNING"] == 1
        assert fixture_counter_log_1.report["/api/v1/reviews/"]["CRITICAL"] == 0
        assert fixture_counter_log_1.report["/api/v1/reviews/1"]["CRITICAL"] == 1


    @pytest.mark.asyncio
    async def test_report_files(self, fixture_counter_log_2) -> None:
        await fixture_counter_log_2.create_report()
        assert fixture_counter_log_2.report["/api/v1/reviews/"]["INFO"] == 6
        assert fixture_counter_log_2.report["/api/v1/reviews/"]["ERROR"] == 1
        assert fixture_counter_log_2.report["/api/v1/reviews/"]["WARNING"] == 1
        assert fixture_counter_log_2.report["/api/v1/reviews/"]["CRITICAL"] == 0
        assert fixture_counter_log_2.report["/api/v1/reviews/1"]["CRITICAL"] == 1

