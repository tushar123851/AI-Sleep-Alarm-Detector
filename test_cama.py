import cv2

from detector.camera import Camera


camera = Camera()

while True:

    frame = camera.read_frame()

    if frame is None:
        break

    cv2.imshow("AI Sleep Alarm Detector", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

camera.release()

cv2.destroyAllWindows()