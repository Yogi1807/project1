from rest_framework import serializers
from core.models import JobDescription, JobTitle, Portal


class JobTitleSerializer(serializers.ModelSerializer):
    """
    Serializer class for JobTitle list view
    """
    class Meta:
        model = JobTitle
        fields = ["id", "title"]
        read_only_fields = ["id"]


class JobDescriptionSerializer(JobTitleSerializer):
    """
    Serializer class for JobTitle detail view
    WE will reuse functionality written under `JobTitleSerializer`
    By these means, we are avoiding duplicates in code.
    Writing nested serializers
    - TODO - refer ->
    - https://www.django-rest-framework.org/api-guide/serializers/#overriding-serialization-and-deserialization-behavior
    """

    class Meta(JobTitleSerializer.Meta):
        fields = JobTitleSerializer.Meta.fields + ["job_description", "portal"]
