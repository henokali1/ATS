# ATS/urls.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include # Make sure include is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the URLs from the duty_hour_log app under the 'logs/' prefix
    path('logs/', include('duty_hour_log.urls')),
    # Optional: Redirect the root URL ('/') to the log list
    path('', lambda request: redirect('log_list', permanent=False)), # Requires from django.shortcuts import redirect
]

# Make sure to add the redirect import if you use the root URL redirection:
# from django.shortcuts import redirect