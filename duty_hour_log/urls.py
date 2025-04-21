# duty_hour_log/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # List & Create view (e.g., /logs/) - Handles both GET (list) and POST (create)
    path('', views.log_list, name='log_list'),

    # Detail view (e.g., /logs/5/)
    path('<int:pk>/', views.log_detail, name='log_detail'),

    # Create view - NO LONGER NEEDED for the primary workflow
    # path('new/', views.log_create, name='log_create'), # Commented out or remove

    # Update view (e.g., /logs/5/edit/)
    path('<int:pk>/edit/', views.log_update, name='log_update'),

    # Delete view (e.g., /logs/5/delete/)
    path('<int:pk>/delete/', views.log_delete, name='log_delete'),
]