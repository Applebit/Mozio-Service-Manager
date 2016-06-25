from django.http import Http404
from django.forms.models import model_to_dict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from serviceprovider.models import Provider, Polygon, Coordinate
from serviceprovider.serializers import ProviderSerializer, PolygonSerializer, CoordinateSerializers


# Create your views here.


class ProviderList(APIView):
    """
    List all provider, or create a new snippet.
    """
    def get(self, request):
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderDetail(APIView):
    """
    Retrieve, update or delete a provider instance.
    """
    def get_object(self, pk):
        try:
            return Provider.objects.get(pk=pk)
        except Provider.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        provider = self.get_object(pk)
        serializer = ProviderSerializer(provider)
        return Response(serializer.data)

    def put(self, request, pk):
        provider = self.get_object(pk)
        serializer = ProviderSerializer(provider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        provider = self.get_object(pk)
        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PolygonList(APIView):
    """
    List all polygon, or create a new snippet.
    """

    def get(self, request):

        objects = Coordinate.objects.select_related('polygon').values('long', 'lat', 'polygon__name', 'polygon__price',  'polygon__provider__name')
        return Response(objects)

    def post(self, request):
        """
        :param request: this api creates a polygon object. it recieves a list of x,y coordinates in key parameter 'geometry' .

        :return:
        """
        if not request.data.get('geometry'):
            return Response("Please Provide Polygon corrdinates in form of an array of two element tuples with x= x-corrdinate, y=y-coordinate", status=status.HTTP_400_BAD_REQUEST)
        coordinates = request.data.get('geometry')
        keys = [u'name', u'price', u'provider']
        data = {key: request.data.get(key) for key in keys}
        serializer = PolygonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            entry_coordinates(serializer.data['id'], coordinates)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def entry_coordinates(id, coordinates):
    """
    This function makes entries in coordinates table for given polygon_id
    :param id: id of the created polygon object
    :param coordinates:  list of corrdinates [{x:23.56, y:67}, {x:12, y:45}, {x:11, y:76}, {x:10, y:44}]
    :return: None
    """
    data = [{'polygon' : id, 'lat': c['x'], 'long': c['y']} for c in coordinates]
    serializer = CoordinateSerializers(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPolygonData(APIView):
    """
     The API to fetch all polygons with  their coordinates matching a given lat, long
    """
    def post(self, request):
        lat = request.data.get('lat')
        long = request.data.get('long')
        objects = Coordinate.objects.select_related('polygon').values('long', 'lat', 'polygon__name', 'polygon__price',  'polygon__provider__name').filter(lat=lat, long=long)
        return Response(objects)


