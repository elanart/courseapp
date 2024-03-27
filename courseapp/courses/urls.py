from django.urls import path, include
from courses import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('lessons', views.LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    # path('lessons/<int:lesson_id>/comments/', views.CommentAPIView.as_view()),
]