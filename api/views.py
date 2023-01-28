from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from .models import Subject, Course
from .permissions import IsEnrolled
from .serializers import SubjectSerializer, CourseSerializer
from rest_framework import viewsets


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseEnrollView(APIView):
    authentication_classes = (BasicAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        if request.user in course.students.all():
            raise ValidationError('you have already registered')
        course.students.add(request.user)
        return Response(
            {"enrolled": True}
        )


class CourseWithContentsSerializer:
    pass


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        if request.user in course.students.all():
            raise ValidationError('you have already registered')
        course.students.add(request.user)
        return Response(
            {'enroll': True}
        )

    @action(detail=True,
            methods=['get'],
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=(permissions.IsAuthenticated, IsEnrolled))
    def contents(self, request, *args, **kwargs):
        print(self.get_serializer())
        return self.retrieve(request, *args, **kwargs)
