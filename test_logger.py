from utils.logger import SleepLogger

logger = SleepLogger()

logger.log(

    ear=0.18,

    status="SLEEPING",

    blink_count=12,

    sleep_events=3,

    alarm="YES"

)

print("Log Saved Successfully")