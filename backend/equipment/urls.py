from django.urls import path
from .views import upload_csv, history, download_report


urlpatterns = [
    path('upload/', upload_csv),
    path('history/', history),
    path('download-report/', download_report),

]
