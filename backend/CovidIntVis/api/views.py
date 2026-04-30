from rest_framework import viewsets
from .serializers import WeeklyDataSerializer, CountyInfectionSerializer, CountySerializer
from ..models import WeeklyData, County, CountyInfection

class WeeklyDataViewSet(viewsets.ModelViewSet):
    queryset = WeeklyData.objects.all()
    serializer_class = WeeklyDataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        date = self.request.query_params.get("date")

        if date:
            queryset = queryset.filter(date=date)
            
        return queryset
        

class CountyViewSet(viewsets.ModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer

class CountyInfectionViewSet(viewsets.ModelViewSet):
    queryset = CountyInfection.objects.all()
    serializer_class = CountyInfectionSerializer