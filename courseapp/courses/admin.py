from django.contrib import admin
from django.db.models import Count
from courses.models import Category, Course, Lesson
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from django.template.response import TemplateResponse

# Register your models here.


class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khoá học trực tuyến'

    def get_urls(self):
        return [
        path('course-stats/', self.stats_view)
        ] + super().get_urls()
    
    def stats_view(self, request):
        count = Course.objects.filter(active=True).count()
        stats = Course.objects\
        .annotate(lesson_count=Count('my_lesson'))\
        .values('id', 'subject', 'lesson_count')
        return TemplateResponse(request, 
        'admin/course-stats.html', {
        'course_count': count,
        'course_stats': stats
        })


class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    fk_name = 'course'


class LessonTagInlineAdmin(admin.TabularInline):
    model = Lesson.tags.through


class TagAdmin(admin.ModelAdmin):
    inlines = [LessonTagInlineAdmin, ]


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
    inlines = [LessonTagInlineAdmin, ]

    class Media:
        css = {
        'all': ('/static/css/style.css', )
        }
        js = ('/static/js/script.js', )


class CourseAdmin(admin.ModelAdmin):
    # list_display = ['id', 'subject', 'description']
    readonly_fields = ['avatar']
    inlines = [LessonInlineAdmin, ]

    def avatar(self, obj):
        if obj:
            return mark_safe('<img src="/static/{url}" width="120" />'.format(url=obj.image.name))

admin_site = CourseAppAdminSite(name='myadmin')
admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
