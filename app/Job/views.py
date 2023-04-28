from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
# from rest_framework import viewsets
from .serializers import JobTitleSerializer, JobDescriptionSerializer
from rest_framework import serializers

from core.models import JobTitle


# Create your views here.


class JobTitleViewSet(ModelViewSet):
    """
    /api/jobtitle (plural)
    /api/jobtitle/481241 (singular)
    """

    serializer_class = JobDescriptionSerializer
    queryset = JobTitle.objects.all()

    def get_serializer_class(self):

        if self.action == "list":
            return JobTitleSerializer
        return self.serializer_class

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer_obj):
        """
        create JObTitle
        """
        serializer_obj.save(user=self.request.user)
