from rest_framework import serializers

from .models import Challenge


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'difficulty', 'created_at']
        read_only_fields = ['id', 'created_at']