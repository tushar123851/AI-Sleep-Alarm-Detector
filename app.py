"""
=====================================================
AI Sleep Alarm Detector
Main FastAPI Application

Author  : Tushar Vala
Version : 1.0.0
=====================================================
"""

# =====================================================
# IMPORTS
# =====================================================

import cv2
import time

from threading import Lock
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import (
    HTMLResponse,
    StreamingResponse,
    JSONResponse
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from detector.camera import Camera
from detector.face_detector import FaceDetector
from detector.eye_detector import EyeDetector
from detector.sleep_detector import SleepDetector
from detector.alarm import Alarm

from utils.logger import SleepLogger
from utils.config import APP_NAME, VERSION


# =====================================================
# APPLICATION OBJECTS
# =====================================================

camera = Camera()

face_detector = FaceDetector()

eye_detector = EyeDetector()

sleep_detector = SleepDetector()

alarm = Alarm()

logger = SleepLogger()


# =====================================================
# GLOBAL VARIABLES
# =====================================================

frame_lock = Lock()

statistics_lock = Lock()

current_frame = None

previous_status = "AWAKE"

detection_running = True

fps = 0.0

previous_time = time.time()


statistics = {
    "status": "AWAKE",
    "ear": 0.0,
    "blink_count": 0,
    "sleep_events": 0,
    "alarm": "OFF",
    "running_time": 0,
    "fps": 0.0
}


# =====================================================
# LIFESPAN
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("=" * 60)
    print(APP_NAME)
    print(f"Version : {VERSION}")
    print("Application Started Successfully")
    print("=" * 60)

    yield

    print("\nClosing Application...")

    try:
        alarm.stop()
    except Exception as error:
        print(f"Alarm shutdown error: {error}")

    try:
        camera.release()
    except Exception as error:
        print(f"Camera shutdown error: {error}")

    try:
        cv2.destroyAllWindows()
    except Exception as error:
        print(f"OpenCV shutdown error: {error}")

    print("Resources Released Successfully")


# =====================================================
# FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="Real-Time AI Sleep Alarm Detector",
    lifespan=lifespan
)


# =====================================================
# STATIC FILES
# =====================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# =====================================================
# TEMPLATES
# =====================================================

templates = Jinja2Templates(
    directory="templates"
)


# =====================================================
# FRAME PROCESSING
# =====================================================

def process_frame(frame):

    global previous_status
    global statistics

    try:

        # -------------------------------------------------
        # FACE LANDMARK DETECTION
        # -------------------------------------------------

        landmarks = face_detector.get_landmarks(frame)

        if landmarks is None:

            cv2.putText(
                frame,
                "Face Not Detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            with statistics_lock:

                statistics["status"] = "NO FACE"

                statistics["ear"] = 0.0

                statistics["alarm"] = "OFF"

            return frame


        # -------------------------------------------------
        # DRAW EYES
        # -------------------------------------------------

        eye_detector.draw_eyes(
            frame,
            landmarks
        )


        # -------------------------------------------------
        # CALCULATE EAR
        # -------------------------------------------------

        left_ear, right_ear, ear = (

            eye_detector.calculate_ear(
                landmarks
            )

        )


        # -------------------------------------------------
        # SLEEP DETECTION
        # -------------------------------------------------

        status = sleep_detector.update(
            ear
        )


        stats = sleep_detector.get_statistics()


        # -------------------------------------------------
        # ALARM CONTROL
        # -------------------------------------------------

        if status == "SLEEPING":

            if not alarm.status()["playing"]:

                alarm.play()

        else:

            alarm.stop()


        # -------------------------------------------------
        # LOG ONLY NEW SLEEP EVENT
        # -------------------------------------------------

        if (

            status == "SLEEPING"

            and

            previous_status != "SLEEPING"

        ):

            logger.log(

                ear=ear,

                status=status,

                blink_count=stats["blink_count"],

                sleep_events=stats["sleep_events"],

                alarm="YES"

            )


        previous_status = status


        # -------------------------------------------------
        # UPDATE STATISTICS
        # -------------------------------------------------

        with statistics_lock:

            statistics["status"] = status

            statistics["ear"] = round(
                ear,
                3
            )

            statistics["blink_count"] = (

                stats["blink_count"]

            )

            statistics["sleep_events"] = (

                stats["sleep_events"]

            )

            statistics["running_time"] = (

                stats["running_time"]

            )

            statistics["alarm"] = (

                "ON"

                if alarm.status()["playing"]

                else

                "OFF"

            )


        # -------------------------------------------------
        # DISPLAY COLOR
        # -------------------------------------------------

        if status == "SLEEPING":

            color = (0, 0, 255)

        else:

            color = (0, 255, 0)


        # -------------------------------------------------
        # DISPLAY INFORMATION
        # -------------------------------------------------

        cv2.putText(

            frame,

            f"EAR : {ear:.3f}",

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            color,

            2

        )


        cv2.putText(

            frame,

            f"Status : {status}",

            (20, 80),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            color,

            2

        )


        cv2.putText(

            frame,

            f"Blinks : {stats['blink_count']}",

            (20, 120),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (255, 255, 0),

            2

        )


        cv2.putText(

            frame,

            f"Sleep Events : {stats['sleep_events']}",

            (20, 160),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (255, 255, 0),

            2

        )


        cv2.putText(

            frame,

            f"Alarm : {statistics['alarm']}",

            (20, 200),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 255, 255),

            2

        )


        return frame


    except Exception as error:

        print(
            f"Frame Processing Error: {error}"
        )

        cv2.putText(

            frame,

            "Processing Error",

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0, 0, 255),

            2

        )

        return frame


# =====================================================
# VIDEO STREAM GENERATOR
# =====================================================

def generate_frames():

    global fps

    global previous_time

    global current_frame


    while True:


        # -------------------------------------------------
        # STOP DETECTION
        # -------------------------------------------------

        if not detection_running:

            time.sleep(0.1)

            continue


        # -------------------------------------------------
        # READ CAMERA FRAME
        # -------------------------------------------------

        frame = camera.read_frame()


        if frame is None:

            time.sleep(0.05)

            continue


        # -------------------------------------------------
        # PROCESS FRAME
        # -------------------------------------------------

        frame = process_frame(
            frame
        )


        # -------------------------------------------------
        # FPS CALCULATION
        # -------------------------------------------------

        current_time = time.time()

        elapsed_time = (

            current_time

            -

            previous_time

        )


        if elapsed_time > 0:

            fps = 1 / elapsed_time


        previous_time = current_time


        # -------------------------------------------------
        # UPDATE FPS STATISTICS
        # -------------------------------------------------

        with statistics_lock:

            statistics["fps"] = round(
                fps,
                1
            )


        # -------------------------------------------------
        # FPS OVERLAY
        # -------------------------------------------------

        cv2.putText(

            frame,

            f"FPS : {fps:.1f}",

            (20, 240),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (255, 255, 255),

            2

        )


        # -------------------------------------------------
        # SAVE CURRENT FRAME
        # -------------------------------------------------

        with frame_lock:

            current_frame = frame.copy()


        # -------------------------------------------------
        # JPEG ENCODING
        # -------------------------------------------------

        success, buffer = cv2.imencode(

            ".jpg",

            frame

        )


        if not success:

            continue


        frame_bytes = buffer.tobytes()


        # -------------------------------------------------
        # STREAM FRAME
        # -------------------------------------------------

        yield (

            b"--frame\r\n"

            b"Content-Type: image/jpeg\r\n\r\n"

            + frame_bytes

            + b"\r\n"

        )


# =====================================================
# HOME PAGE
# =====================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    # IMPORTANT:
    # This version avoids the TemplateResponse
    # compatibility issue in your current environment.

    template = templates.get_template(
        "index.html"
    )

    html_content = template.render(

        request=request,

        title=APP_NAME

    )

    return HTMLResponse(
        content=html_content
    )


# =====================================================
# VIDEO FEED
# =====================================================

@app.get("/video")
def video():

    return StreamingResponse(

        generate_frames(),

        media_type="multipart/x-mixed-replace; boundary=frame"

    )


# =====================================================
# STATISTICS API
# =====================================================

@app.get("/statistics")
def statistics_api():

    with statistics_lock:

        return JSONResponse(

            content={

                "status": statistics["status"],

                "ear": statistics["ear"],

                "blink_count": statistics["blink_count"],

                "sleep_events": statistics["sleep_events"],

                "alarm": statistics["alarm"],

                "running_time": statistics["running_time"],

                "fps": statistics["fps"]

            }

        )


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health():

    return {

        "status": "Running",

        "application": APP_NAME,

        "version": VERSION,

        "camera": "Connected"

    }


# =====================================================
# START DETECTION
# =====================================================

@app.post("/start")
def start_detection():

    global detection_running

    detection_running = True

    return {

        "success": True,

        "message": "Detection Started"

    }


# =====================================================
# STOP DETECTION
# =====================================================

@app.post("/stop")
def stop_detection():

    global detection_running

    detection_running = False

    alarm.stop()

    with statistics_lock:

        statistics["status"] = "STOPPED"

        statistics["alarm"] = "OFF"


    return {

        "success": True,

        "message": "Detection Stopped"

    }


# =====================================================
# RESET STATISTICS
# =====================================================

@app.post("/reset")
def reset_statistics():

    global statistics

    global previous_status

    sleep_detector.reset()

    alarm.stop()

    previous_status = "AWAKE"


    with statistics_lock:

        statistics = {

            "status": "AWAKE",

            "ear": 0.0,

            "blink_count": 0,

            "sleep_events": 0,

            "alarm": "OFF",

            "running_time": 0,

            "fps": 0.0

        }


    return {

        "success": True,

        "message": "Statistics Reset Successfully"

    }


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app:app",

        host="127.0.0.1",

        port=8000,

        reload=False

    )