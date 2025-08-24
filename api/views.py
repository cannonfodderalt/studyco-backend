from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudySpot, Criteria, SpotCriteria, Score, BusynessLevel
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend


# StudySpot ViewSet
class StudySpotViewSet(viewsets.ModelViewSet):
    queryset = StudySpot.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':     # /api/studyspots/
            return serializers.SpotSerializer
        if self.action == 'retrieve': # /api/studyspots/<id>/
            return serializers.SpotDetailSerializer
        return serializers.SpotDetailSerializer


# Criteria ViewSet
class CriteriaViewSet(viewsets.ModelViewSet):
    queryset = Criteria.objects.all()
    serializer_class = serializers.CriteriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['attribute']


# SpotCriteria ViewSet
class SpotCriteriaViewSet(viewsets.ModelViewSet):
    queryset = SpotCriteria.objects.all()
    serializer_class = serializers.SpotCriteriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['studySpot', 'criteria']


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = serializers.ScoreSerializer

class BusynessLevelViewSet(viewsets.ModelViewSet):
    queryset = BusynessLevel.objects.all()
    serializer_class = serializers.BusynessLevelSerializer