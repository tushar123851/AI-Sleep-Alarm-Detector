"""
=====================================================
AI Sleep Alarm Detector
Logger Module

Author : Tushar Vala
=====================================================
"""

import csv
from pathlib import Path
from datetime import datetime

from utils.config import LOG_FILE


class SleepLogger:

    def __init__(self):

        self.log_file = Path(LOG_FILE)

        self.log_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.log_file.exists():

            with open(
                self.log_file,
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Date",
                    "Time",
                    "EAR",
                    "Status",
                    "Blink Count",
                    "Sleep Events",
                    "Alarm"
                ])

    # ------------------------------------------

    def log(
        self,
        ear,
        status,
        blink_count,
        sleep_events,
        alarm
    ):

        now = datetime.now()

        with open(
            self.log_file,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                round(ear,3),
                status,
                blink_count,
                sleep_events,
                alarm
            ])