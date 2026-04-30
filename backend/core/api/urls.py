from rest_framework.routers import DefaultRouter
from django.urls import path, include
from CovidIntVis.api.urls import data_router

router = DefaultRouter()

router.registry.extend(data_router.registry)

urlpatterns = [
    path('', include(router.urls)),
]