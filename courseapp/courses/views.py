from sqlite3 import IntegrityError
import statistics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from courses.models import Course, Lesson, Comment
from courses.serializers import CourseSerializer, LessonSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def index(request):
    return HttpResponse("e-Course App")


class CourseViewSet(viewsets.ModelViewSet):    
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class LessonViewSet(viewsets.ViewSet):
    def list(self, request):
        lessons = Lesson.objects.filter(active=True)
        serializer = LessonSerializer(lessons, many=True)
        return Response(data=serializer.data)

    def create(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(pk=pk)
            serializer = LessonSerializer(lesson)
            return Response(serializer.data)
        except Lesson.DoesNotExist:
            raise Http404()

    def update(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(pk=pk)
            serializer = LessonSerializer(lesson, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Lesson.DoesNotExist:
            raise Http404()

    def partial_update(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(pk=pk)
            serializer = LessonSerializer(lesson, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Lesson.DoesNotExist:
            raise Http404()

    def destroy(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(pk=pk)
            lesson.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Lesson.DoesNotExist:
            raise Http404()
        
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        
        return [IsAdminUser()]


# class CommentAPIView(APIView):
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
        
#         return [permissions.IsAuthenticated()]
    
#     def get(self, request, lesson_id):
#         comments = Comment.objects.filter(lesson_id=lesson_id)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data, status=statistics.HTTP_200_OK)

#     def post(self, request, lesson_id):
#         content = request.data.get('content')
#         if content is not None:
#             try:
#                 c = Comment.objects.create(content=content, user=request.user, lesson_id=lesson_id)
#             except IntegrityError:
#                 err_msg = "Lesson does not exist!"
#             else:
#                 return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)
#         else:
#             err_msg = "Content is required!!!"
            
#         return Response(data={'error_msg': err_msg}, status=status.HTTP_400_BAD_REQUEST)