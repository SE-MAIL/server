from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recommended/shower/personaldata/<pk>/', views.PersonalShowerEmissionAPIView.as_view()),
    path('recommended/shower/dataset/<pk>/', views.ShowerdatasetEmissionAPIView.as_view()),
]
