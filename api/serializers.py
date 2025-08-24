from rest_framework import serializers
from .models import StudySpot, Criteria, SpotCriteria, Score, BusynessLevel

class SpotSerializer(serializers.ModelSerializer):
    criteria = serializers.SerializerMethodField()

    class Meta:
        model = StudySpot
        fields = ['id', 'name', 'latitude', 'longitude', 'criteria']

    def get_criteria(self, spot):
        criteria = Criteria.objects.filter(
            id__in=SpotCriteria.objects.filter(studySpot=spot).values_list('criteria', flat=True)
        )
        return CriteriaSerializer(criteria, many=True).data

    
class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = '__all__'
    
    
class SpotCriteriaSerializer(serializers.ModelSerializer):
    studySpot = SpotSerializer(read_only=True)
    criteria = CriteriaSerializer(read_only=True)

    class Meta:
        model = SpotCriteria
        fields = '__all__'
        
class SpotDetailSerializer(serializers.ModelSerializer):
    criteria = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = StudySpot
        fields = ['id', 'name', 'latitude', 'longitude', 'criteria', 'image_url']

    def get_criteria(self, spot):
        criteria = Criteria.objects.filter(
            id__in=SpotCriteria.objects.filter(studySpot=spot).values_list('criteria', flat=True)
        )
        return CriteriaSerializer(criteria, many=True).data

    def get_image_url(self, spot):
        return spot.get_image_urls()
    
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"

class BusynessLevelSerializer(serializers.ModelSerializer):
    studySpot = serializers.PrimaryKeyRelatedField(queryset=StudySpot.objects.all())
    score = serializers.PrimaryKeyRelatedField(queryset=Score.objects.all())

    class Meta:
        model = BusynessLevel
        fields = "__all__"
