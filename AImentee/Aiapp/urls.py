from django.urls import path
from . import views

urlpatterns = [
    # path('speech/', views.load_data, name='resume_view'),
    path('home/', views.load_home_page, name='load_home_page'),
    # path('speech_to_text/', views.recognize_speech, name='speech_to_text'),
]

