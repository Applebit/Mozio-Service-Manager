from django.http import Http404
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
    def get_object(self, email):
        try:
            return Provider.objects.get(pk=email)
        except Provider.DoesNotExist:
            raise Http404

    def get(self, request, email):
        provider = self.get_object(email)
        serializer = ProviderSerializer(provider)
        return Response(serializer.data)

    def put(self, request, email):
        provider = self.get_object(email)
        serializer = ProviderSerializer(provider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, email):
        provider = self.get_object(email)
        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PolygonList(APIView):
    """
    List all polygon, or create a new snippet.
    """

    def get(self, request):
        polygon = Polygon.objects.all()
        serializer = PolygonSerializer(polygon, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolygonDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Polygon.objects.get(pk=pk)
        except Polygon.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        polygon = self.get_object(pk)
        serializer = ProviderSerializer(polygon)
        return Response(serializer.data)

    def put(self, request, pk):
        polygon = self.get_object(pk)
        serializer = ProviderSerializer(polygon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        polygon = self.get_object(pk)
        polygon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CoordinateList(APIView):
    """
        List all polygon, or create a new snippet.
        """

    def get(self, request):
        polygon = Polygon.objects.all()
        serializer = PolygonSerializer(polygon, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
