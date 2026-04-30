from rest_framework import serializers
from ..models import WeeklyData, County, CountyInfection

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ['id', 'name', 'geometry']

class CountyInfectionSerializer(serializers.ModelSerializer):
    county_id = serializers.PrimaryKeyRelatedField(
        queryset=County.objects.all(), source="county", write_only=True
    )
    county = CountySerializer(read_only=True)

    class Meta:
        model = CountyInfection
        fields = ["id", "county_id", "county", "infections"]

class WeeklyDataSerializer(serializers.ModelSerializer):
    county_data = CountyInfectionSerializer(many=True)

    class Meta:
        model = WeeklyData
        fields = ["id", "date", "county_data"]
        extra_kwargs = {
            "date": {
                "validators": []
            }
        }

    def create(self, validated_data):
        county_data = validated_data.pop("county_data")

        weekly_data, created = WeeklyData.objects.update_or_create(
            date=validated_data["date"],
            defaults=validated_data
        )

        weekly_data.county_data.all().delete()

        for item in county_data:
            CountyInfection.objects.create(
                weekly_data=weekly_data,
                **item
            )

        return weekly_data
