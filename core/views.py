from rest_framework import viewsets

from .models import Challenge
from .serializers import ChallengeSerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all().order_by('-created_at')
    serializer_class = ChallengeSerializer