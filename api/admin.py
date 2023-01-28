from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from api.models import Subject, Course, Module, Content
from rest_framework.renderers import JSONRenderer
# Register your models here.
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Content)
admin.site.register(ContentType)
