from django.shortcuts import render
from rest_framework import viewsets

from .models import Challenge
from .serializers import ChallengeSerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


def index(request):
    return render(request, 'core/index.html')
