from datetime import datetime
import pytz
def is_time_between(start_hour, end_hour):
    """
    Check whether current IST time is within the given range.
    """
    ist = pytz.timezone("Asia/Kolkata")
    current = datetime.now(ist).hour
    return start_hour <= current < end_hour
