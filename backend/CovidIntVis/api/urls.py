from rest_framework.routers import DefaultRouter
from .views import WeeklyDataViewSet, CountyViewSet, CountyInfectionViewSet

data_router = DefaultRouter()

data_router.register(r"weekly-data", WeeklyDataViewSet, basename="weekly-data")
data_router.register(r"counties", CountyViewSet, basename="counties")
data_router.register(r"infections", CountyInfectionViewSet, basename="infections")

urlpatterns = data_router.urls