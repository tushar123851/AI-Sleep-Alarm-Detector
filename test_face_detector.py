import cv2

from detector.camera import Camera
from detector.face_detector import FaceDetector


camera = Camera()
detector = FaceDetector()

while True:

    frame = camera.read_frame()

    if frame is None:
        break

    results = detector.detect(frame)

    frame = detector.draw_landmarks(frame, results)

    cv2.imshow("Face Detector", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

camera.release()

cv2.destroyAllWindows()