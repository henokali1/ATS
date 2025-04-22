# duty_hour_log/templatetags/duration_tags.py
from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='format_duration')
def format_duration(value):
    """Formats a timedelta object into HH:MM string."""
    if not isinstance(value, timedelta):
        return "-" # Return dash if input is not a timedelta (e.g., None)

    total_seconds = int(value.total_seconds())

    # Handle negative durations if they somehow occur (shouldn't with model logic)
    if total_seconds < 0:
        return "-:--" # Or indicate error

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    # seconds = total_seconds % 60 # We only need HH:MM

    return f"{hours:02d}:{minutes:02d}"