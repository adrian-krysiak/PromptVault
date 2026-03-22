from rest_framework import serializers
from .models import Prompt


class PromptReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ("id", "title", "content", "created_at", "updated_at")
        read_only_fields = fields


class PromptWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ("title", "content")