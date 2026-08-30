import cv2

from detector.camera import Camera
from detector.face_detector import FaceDetector
from detector.eye_detector import EyeDetector
from detector.sleep_detector import SleepDetector


camera = Camera()

face_detector = FaceDetector()

eye_detector = EyeDetector()

sleep_detector = SleepDetector()


while True:

    frame = camera.read_frame()

    if frame is None:
        break

    landmarks = face_detector.get_landmarks(frame)

    if landmarks is not None:

        eye_detector.draw_eyes(frame, landmarks)

        _, _, ear = eye_detector.calculate_ear(landmarks)

        status = sleep_detector.update(ear)

        stats = sleep_detector.get_statistics()

        color = (0,255,0)

        if status == "SLEEPING":
            color = (0,0,255)

        cv2.putText(
            frame,
            f"EAR : {ear:.3f}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        cv2.putText(
            frame,
            f"Status : {status}",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        cv2.putText(
            frame,
            f"Blinks : {stats['blink_count']}",
            (20,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Sleep Events : {stats['sleep_events']}",
            (20,160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,0),
            2
        )

    cv2.imshow("AI Sleep Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()

cv2.destroyAllWindows()