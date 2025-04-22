# duty_hour_log/utils.py
from datetime import timedelta

def format_timedelta_to_hhmm(value):
    """Formats a timedelta object into HH:MM string."""
    if not isinstance(value, timedelta):
        return "-" # Return dash if input is not a timedelta (e.g., None)

    total_seconds = int(value.total_seconds())

    # Handle negative durations if they somehow occur
    if total_seconds < 0:
        # Or handle as error, e.g., return "-:--" or raise ValueError
        hours = total_seconds // 3600
        minutes = abs((total_seconds % 3600) // 60) # Keep minutes positive
    else:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

    # Format, ensuring two digits for minutes
    return f"{hours}:{minutes:02d}"