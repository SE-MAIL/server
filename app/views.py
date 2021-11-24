from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.response import Response
from .models import Showerdataset
from .models import Showerlog
from .serializer import ShowerdatasetSerializer
from .serializer import ShowerlogSerializer

# Create your views here.

class ShowerdatasetEmissionAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Showerdataset, pk=pk)

    def get(self, request, pk, format=None):
        Showerdataset = self.get_object(pk)
        serializer = ShowerdatasetSerializer(Showerdataset)
        return Response(serializer.data)

class ShowerlogEmissionAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Showerlog, pk=pk)

    def get(self, request, pk, format=None):
        Showerlog = self.get_object(pk)
        serializer = ShowerlogSerializer(Showerlog)
        return Response(serializer.data)
    
    def put(self, request, pk):
        Showerlog = self.get_object(pk)
        serializer = ShowerlogSerializer(Showerlog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)