# duty_hour_log/admin.py
from django.contrib import admin
from .models import Initial, DutyHourLog

@admin.register(Initial)
class InitialAdmin(admin.ModelAdmin):
    list_display = ('code', 'full_name', 'is_active')
    search_fields = ('code', 'full_name')
    list_filter = ('is_active',)

@admin.register(DutyHourLog)
class DutyHourLogAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'op', 'initial', 'trainee', 'ojti', 'examiner', # Added trainee, reordered for clarity
        'rating', 'start_time', 'finish_time', 'created_at'
    )
    list_filter = ('date', 'op', 'initial', 'trainee', 'ojti', 'examiner', 'rating')
    search_fields = ('initial__code', 'trainee__code', 'ojti__code', 'examiner__code', 'remarks')
    date_hierarchy = 'date'
    raw_id_fields = ('initial', 'ojti', 'examiner', 'trainee',)