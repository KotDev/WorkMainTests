import os.path
from typing import List
import re
import asyncio
import sys


class CounterLogs:
    def __init__(self, logs_level: List[str], path_files: List[str], flag: str) -> None:
        self.logs_level: List[str] = logs_level
        self.path_files: List[str] = path_files
        self.flag: str = flag
        self.total_counter: int = 0
        self.report: dict = dict()

        for file in self.path_files:
            if not os.path.exists(os.path.abspath(file)):
                raise ValueError(f"such {file} does not exists in folder logs")


    async def counters_log(self, file: str) -> None:
        pattern_log_level = re.compile(rf"({'|'.join(self.logs_level)}).*django\.request")
        pattern_api = re.compile(r"django\.request:.*?(\S+/\S+)")
        with open(file, "r") as f:
            for log in f:
                log_level = re.search(pattern_log_level, log)
                if log_level:
                    log_level = log_level.group(1)
                    api = re.search(pattern_api, log)
                    if api:
                        api = api.group(1)
                        self.total_counter += 1
                        if api not in self.report:
                            self.report[api] = {log_level: 0 for log_level in self.logs_level}
                            self.report[api][log_level] += 1
                        elif self.report.get(api) is not None:
                            self.report[api][log_level] += 1

    async def create_report(self) -> None:
        tasks = [self.counters_log(file) for file in self.path_files]
        await asyncio.gather(*tasks)

    async def print_report(self) -> None:
        print(f"Total requests: {self.total_counter}")
        header = f"{self.flag.upper()[2:]:<20}" + "".join(f"{level:<10}" for level in self.logs_level)
        print(header)
        for api_path, levels in self.report.items():
            row = f"{api_path:<20}"
            for level in self.logs_level:
                row += f"{levels.get(level, 0):<10}"
            print(row)



async def main():
    levels_report = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    args = sys.argv[1:]
    files = [f"src/logs/{file}" for file in args[:-1]]
    logger = CounterLogs(logs_level=levels_report, path_files=files, flag=args[-1])
    await logger.create_report()
    await logger.print_report()

if __name__ == '__main__':
    asyncio.run(main())





