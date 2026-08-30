"""
=====================================================
AI Sleep Alarm Detector
Alarm Module

Author : Tushar Vala
=====================================================
"""

import os
import threading
import pygame


class Alarm:
    """
    Alarm Controller
    """

    def __init__(self, alarm_file="static/audio/alarm.mp3"):

        pygame.mixer.init()

        self.alarm_file = alarm_file

        self.is_playing = False

    # =================================================

    def play(self):

        if self.is_playing:
            return

        if not os.path.exists(self.alarm_file):

            print(f"Alarm file not found: {self.alarm_file}")

            return

        self.is_playing = True

        threading.Thread(
            target=self._play_alarm,
            daemon=True
        ).start()

    # =================================================

    def _play_alarm(self):

        try:

            pygame.mixer.music.load(self.alarm_file)

            pygame.mixer.music.play(-1)

        except Exception as e:

            print("Alarm Error:", e)

            self.is_playing = False

    # =================================================

    def stop(self):

        if not self.is_playing:
            return

        pygame.mixer.music.stop()

        self.is_playing = False

    # =================================================

    def status(self):

        return {

            "playing": self.is_playing

        }