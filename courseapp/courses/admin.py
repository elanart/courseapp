from django.contrib import admin
from courses.models import Category, Course, Lesson
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Register your models here.


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonAdmin(admin.ModelAdmin):
    form = LessonForm 
    # list_display = ['id', 'subject', 'created_date', 'course']
    list_filter = ['subject', 'created_date']
    search_fields = ['subject', 'course__subject']

    class Media:
        css = {
        'all': ('/static/css/style.css', )
        }
        js = ('/static/js/script.js', )


class CourseAdmin(admin.ModelAdmin):
    # list_display = ['id', 'subject', 'description']
    readonly_fields = ['avatar']

    def avatar(self, obj):
        if obj:
            return mark_safe('<img src="/static/{url}" width="120" />'.format(url=obj.image.name))

admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
