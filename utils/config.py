"""
=========================================================
AI Sleep Alarm Detector
Configuration File

Author : Tushar Vala
=========================================================
"""

from pathlib import Path

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"
MODEL_DIR = BASE_DIR / "models"
LOG_DIR = BASE_DIR / "logs"

# -------------------------------------------------
# Camera Configuration
# -------------------------------------------------

CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 30

# -------------------------------------------------
# Face Detection
# -------------------------------------------------

MAX_FACES = 1

REFINE_LANDMARKS = True

MIN_DETECTION_CONFIDENCE = 0.5

MIN_TRACKING_CONFIDENCE = 0.5

# -------------------------------------------------
# Eye Detection
# -------------------------------------------------

EAR_THRESHOLD = 0.22

SLEEP_FRAME_LIMIT = 20

# -------------------------------------------------
# Alarm Configuration
# -------------------------------------------------

ALARM_SOUND = STATIC_DIR / "audio" / "alarm.mp3"

ENABLE_ALARM = True

# -------------------------------------------------
# Logging
# -------------------------------------------------

LOG_FILE = LOG_DIR / "sleep_logs.csv"

SAVE_LOGS = True

# -------------------------------------------------
# Application
# -------------------------------------------------

APP_NAME = "AI Sleep Alarm Detector"

VERSION = "1.0.0"



# -------------------------------------------------
# Face Detection Configuration
# -------------------------------------------------

MAX_FACES = 1

REFINE_LANDMARKS = True

MIN_DETECTION_CONFIDENCE = 0.5

MIN_TRACKING_CONFIDENCE = 0.5