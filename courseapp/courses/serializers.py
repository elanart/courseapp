from rest_framework.serializers import ModelSerializer
from courses.models import Course, Tag, Lesson, Comment


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'created_date', 'category']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'content', 'created_date', 'updated_date', 'tags']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']