from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', views.ShowerlogEmissionAPIView.as_view()),
    path('post/<int:pk>/', views.ShowerdatasetEmissionAPIView.as_view()),
]
