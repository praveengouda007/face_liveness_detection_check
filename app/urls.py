from django.contrib import admin
from django.urls import path, include
# from app.views import UploadViewSet
from rest_framework import routers
from .views import UploadView

urlpatterns = [
    path('', UploadView.as_view()),
]

