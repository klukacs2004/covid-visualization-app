from rest_framework import viewsets
from .serializers import WeeklyDataSerializer, CountyInfectionSerializer, CountySerializer
from ..models import WeeklyData, County, CountyInfection

class WeeklyDataViewSet(viewsets.ModelViewSet):
    queryset = WeeklyData.objects.all()
    serializer_class = WeeklyDataSerializer

class CountyViewSet(viewsets.ModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer

class CountyInfectionViewSet(viewsets.ModelViewSet):
    queryset = CountyInfection.objects.all()
    serializer_class = CountyInfectionSerializer