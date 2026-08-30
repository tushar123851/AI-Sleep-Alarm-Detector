import cv2

from detector.camera import Camera
from detector.face_detector import FaceDetector
from detector.eye_detector import EyeDetector


camera = Camera()
face_detector = FaceDetector()
eye_detector = EyeDetector()


while True:

    frame = camera.read_frame()

    if frame is None:
        break

    landmarks = face_detector.get_landmarks(frame)

    if landmarks is not None:

        eye_detector.draw_eyes(frame, landmarks)

        left, right, avg = eye_detector.calculate_ear(landmarks)

        cv2.putText(
            frame,
            f"EAR : {avg:.3f}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    cv2.imshow(
        "Eye Detector",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()