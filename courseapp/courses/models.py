from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class ModelBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='courses/%Y/%m', null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-id']
    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Course(ModelBase):
    subject = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('subject', 'category')

    def __str__(self):
        return self.subject
    

class Lesson(ModelBase):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', related_query_name='my_lesson')
    tags = models.ManyToManyField('Tag', blank=True, related_name='lessons')

    class Meta:
        unique_together = ('subject', 'course')

    def __str__(self):
        return self.subject
    

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name