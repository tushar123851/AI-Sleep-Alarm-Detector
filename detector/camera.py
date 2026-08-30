"""
=====================================================
AI Sleep Alarm Detector
Camera Module

Author : Tushar Vala
=====================================================
"""

import cv2

from utils.config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FPS
)


class Camera:
    """
    Camera Class

    Handles:
    - Camera Initialization
    - Frame Capture
    - Frame Resize
    - Camera Release
    """

    def __init__(self):

        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        if not self.cap.isOpened():
            raise RuntimeError(
                "Unable to access webcam."
            )

        # Camera Properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, FPS)

    def read_frame(self):
        """
        Read frame from webcam.
        """

        success, frame = self.cap.read()

        if not success:
            return None

        frame = cv2.flip(frame, 1)

        return frame

    def get_resolution(self):
        """
        Return camera resolution.
        """

        width = int(
            self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        return width, height

    def get_fps(self):
        """
        Return camera FPS.
        """

        fps = self.cap.get(
            cv2.CAP_PROP_FPS
        )

        return fps

    def is_open(self):
        """
        Check camera status.
        """

        return self.cap.isOpened()

    def release(self):
        """
        Release camera.
        """

        if self.cap.isOpened():
            self.cap.release()

    def __del__(self):
        """
        Destructor
        """

        self.release()