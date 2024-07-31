from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('initialize_audio_library/', views.initialize_audio_library, name='initialize_audio_library'),
    path('novel_to_GPT/', views.novel_to_GPT, name='novel_to_GPT'),
    path('process_input/', views.process_input, name='process_input'),
    path('process_script/', views.process_script, name='process_script'),
    path('generate_audiobook/', views.generate_audiobook, name='generate_audiobook'),
    path('check_task_status/<str:task_id>/', views.check_task_status, name='check_task_status'),
]
