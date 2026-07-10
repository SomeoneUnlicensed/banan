from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:course_slug>/lessons/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<slug:course_slug>/lessons/<slug:lesson_slug>/complete/', views.lesson_complete, name='lesson_complete'),
    path('courses/<slug:slug>/enroll/', views.enroll, name='enroll'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('register/', views.register, name='register'),
]
