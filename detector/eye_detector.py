"""
=====================================================
AI Sleep Alarm Detector
Eye Detection Module

Author : Tushar Vala
=====================================================
"""

import cv2
import numpy as np


class EyeDetector:
    """
    Eye Detector

    Calculates:
    - Eye Aspect Ratio (EAR)
    - Eye Status (Open/Closed)
    """

    # -----------------------------
    # MediaPipe Eye Landmark Index
    # -----------------------------

    LEFT_EYE = [
        362, 385, 387, 263, 373, 380
    ]

    RIGHT_EYE = [
        33, 160, 158, 133, 153, 144
    ]

    def __init__(self):
        pass

    # ------------------------------------------------

    @staticmethod
    def euclidean_distance(point1, point2):
        """
        Calculate Euclidean Distance
        """
        return np.linalg.norm(point1 - point2)

    # ------------------------------------------------

    def eye_aspect_ratio(self, eye):
        """
        Calculate Eye Aspect Ratio (EAR)
        """

        A = self.euclidean_distance(
            eye[1], eye[5]
        )

        B = self.euclidean_distance(
            eye[2], eye[4]
        )

        C = self.euclidean_distance(
            eye[0], eye[3]
        )

        ear = (A + B) / (2.0 * C)

        return ear

    # ------------------------------------------------

    def calculate_ear(self, landmarks):
        """
        Calculate Left EAR
        Right EAR
        Average EAR
        """

        left_eye = landmarks[self.LEFT_EYE]

        right_eye = landmarks[self.RIGHT_EYE]

        left_ear = self.eye_aspect_ratio(left_eye)

        right_ear = self.eye_aspect_ratio(right_eye)

        average_ear = (left_ear + right_ear) / 2

        return left_ear, right_ear, average_ear

    # ------------------------------------------------

    def draw_eyes(self, frame, landmarks):
        """
        Draw Eye Landmarks
        """

        for index in self.LEFT_EYE:

            cv2.circle(
                frame,
                tuple(landmarks[index]),
                2,
                (0, 255, 0),
                -1
            )

        for index in self.RIGHT_EYE:

            cv2.circle(
                frame,
                tuple(landmarks[index]),
                2,
                (0, 255, 0),
                -1
            )

        return frame