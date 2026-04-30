from os import name

from django.db import models

# Create your models here.
class WeeklyData(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)

class County(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.TextField()

    class Meta:
        unique_together = ('name', 'geometry')

    def __str__(self):
        return str(self.name)
    
class CountyInfection(models.Model):
    weekly_data = models.ForeignKey(WeeklyData, on_delete=models.CASCADE, related_name="county_data")
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="infection_data")
    infections = models.FloatField()

    class Meta:
        unique_together = ("weekly_data", "county")
    
    