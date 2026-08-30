"""
=====================================================
AI Sleep Alarm Detector
Sleep Detection Module

Author : Tushar Vala
=====================================================
"""

import time

from utils.config import (
    EAR_THRESHOLD,
    SLEEP_FRAME_LIMIT
)


class SleepDetector:
    """
    Detect Sleep using Eye Aspect Ratio (EAR)
    """

    def __init__(self):

        self.frame_counter = 0

        self.blink_counter = 0

        self.sleep_counter = 0

        self.total_sleep_events = 0

        self.eye_closed = False

        self.sleeping = False

        self.status = "AWAKE"

        self.start_time = time.time()

    # ------------------------------------------------

    def update(self, ear):
        """
        Update sleep state.
        """

        if ear < EAR_THRESHOLD:

            self.frame_counter += 1

            self.eye_closed = True

            # Sleep detected

            if self.frame_counter >= SLEEP_FRAME_LIMIT:

                if not self.sleeping:

                    self.total_sleep_events += 1

                self.sleeping = True

                self.status = "SLEEPING"

        else:

            # Blink Detection

            if self.eye_closed:

                self.blink_counter += 1

            self.frame_counter = 0

            self.eye_closed = False

            self.sleeping = False

            self.status = "AWAKE"

        return self.status

    # ------------------------------------------------

    def get_status(self):
        """
        Return Current Status
        """

        return self.status

    # ------------------------------------------------

    def is_sleeping(self):
        """
        Returns True if sleeping.
        """

        return self.sleeping

    # ------------------------------------------------

    def get_statistics(self):
        """
        Return Detection Statistics
        """

        return {

            "status": self.status,

            "blink_count": self.blink_counter,

            "sleep_events": self.total_sleep_events,

            "frames_closed": self.frame_counter,

            "running_time": round(
                time.time() - self.start_time,
                2
            )
        }

    # ------------------------------------------------

    def reset(self):
        """
        Reset Detector
        """

        self.frame_counter = 0

        self.blink_counter = 0

        self.sleep_counter = 0

        self.total_sleep_events = 0

        self.eye_closed = False

        self.sleeping = False

        self.status = "AWAKE"