"""
=====================================================
AI Sleep Alarm Detector
Face Detection Module

Author : Tushar Vala
=====================================================
"""

import cv2
import mediapipe as mp
import numpy as np

from utils.config import (
    MAX_FACES,
    REFINE_LANDMARKS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE
)


class FaceDetector:
    """
    MediaPipe Face Mesh Detector
    """

    def __init__(self):

        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=MAX_FACES,
            refine_landmarks=REFINE_LANDMARKS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )

        self.drawer = mp.solutions.drawing_utils

        self.draw_spec = self.drawer.DrawingSpec(
            color=(0, 255, 0),
            thickness=1,
            circle_radius=1
        )

    def detect(self, frame):
        """
        Detect face landmarks.

        Returns:
            results : MediaPipe results
        """

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb)

        return results

    def get_landmarks(self, frame):
        """
        Convert normalized landmarks to pixel coordinates.

        Returns:
            numpy.ndarray of shape (468, 2)
            or None if no face is detected.
        """

        results = self.detect(frame)

        if not results.multi_face_landmarks:
            return None

        face = results.multi_face_landmarks[0]

        h, w, _ = frame.shape

        landmarks = []

        for landmark in face.landmark:

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            landmarks.append((x, y))

        return np.array(landmarks)

    def draw_landmarks(self, frame, results):
        """
        Draw face mesh on frame.
        """

        if not results.multi_face_landmarks:
            return frame

        for face in results.multi_face_landmarks:

            self.drawer.draw_landmarks(
                image=frame,
                landmark_list=face,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=self.draw_spec,
                connection_drawing_spec=self.draw_spec
            )

        return frame

    def face_detected(self, frame):
        """
        Returns True if a face is detected.
        """

        results = self.detect(frame)

        return results.multi_face_landmarks is not None