from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer, TagSerializer

# Create your views here.
def index(request):
    return HttpResponse("e-Course App")


class CourseViewSet(viewsets.ModelViewSet):    
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]