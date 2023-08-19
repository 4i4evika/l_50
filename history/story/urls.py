from django.urls import path
from . import views


app_name = 'story'

urlpatterns = [
    path('', views.story, name='story'),
    path('<int:story_id>/', views.detail, name='detail'),
]
