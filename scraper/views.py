from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from scraper.serializers import ReconSiteSerializer


class ReconSiteView (APIView):
    def post(self , request):
        permission_classes = [IsAuthenticated]
        serializer = ReconSiteSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data , status=200)
        return Response(serializer.errors , status=403)
