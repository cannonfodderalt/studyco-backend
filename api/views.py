from rest_framework import viewsets
from .models import StudySpot, Criteria, SpotCriteria, Score, BusynessLevel
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import action


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

    def get_queryset(self):
        cutoff = timezone.now() - timedelta(hours=3)
        # Clean up old entries (simple approach)
        BusynessLevel.objects.filter(submissionDate__lt=cutoff).delete()
        return super().get_queryset().filter(submissionDate__gte=cutoff)

    @action(detail=True, methods=["get"], url_path="spot")
    def spot_busyness(self, request, pk=None):
        cutoff = timezone.now() - timedelta(hours=3)
        qs = BusynessLevel.objects.filter(
            studySpot_id=pk,
            submissionDate__gte=cutoff
        ).order_by("-submissionDate")

        last_three = qs[:3]

        if not last_three:
            return Response({
                "average": None,
                "last_review": None,
                "reviews": []
            })

        scores = [b.score.rank for b in last_three]
        avg_score = sum(scores) / len(scores)
        last_review = last_three[0].submissionDate

        serializer = self.get_serializer(last_three, many=True)

        return Response({
            "average": round(avg_score, 2),  # rounded to 2 decimals
            "last_review": last_review,
            "reviews": serializer.data
        })
