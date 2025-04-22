# duty_hour_log/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_list, name='log_list'),
    path('save_inline/', views.save_inline_log, name='save_inline_log'),

    # New endpoint for updating existing log inline (finish/remarks)
    path('<int:pk>/update_inline/', views.update_inline_log, name='update_inline_log'),

    path('<int:pk>/', views.log_detail, name='log_detail'),
    path('<int:pk>/edit/', views.log_update, name='log_update'), # Keep standard edit page
    path('<int:pk>/delete/', views.log_delete, name='log_delete'),
    path('report/', views.report_view, name='report_view'),
]