from rest_framework import serializers
from serviceprovider.models import Provider, Polygon, Coordinate


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('name', 'email', 'phone_number', 'language', 'currency')


class PolygonSerializer(serializers.ModelSerializer):
    """

    """
    provider_name = serializers.RelatedField(source='provider', read_only=True)

    class Meta:
        model = Polygon
        fields = ('provider_name','name', 'price', )


class CoordinateSerializers(serializers.ModelSerializer):
    polygon_name = serializers.RelatedField(source='polygon', read_only=True)

    class Meta:
        model = Coordinate
        fields = ('polygon_name','log', 'lat', )