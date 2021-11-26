from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Personalshowerdata, Showerdataset, User
from .models import Showerlog
from .serializer import ShowerdatasetSerializer
from .serializer import ShowerlogSerializer
import logging

# Create your views here.

class ShowerdatasetEmissionAPIView(APIView):
    def get_user(self, pk):
        return get_object_or_404(User, id=pk)

    def get_dataSet(self, pk): # 해당 성별, 나이대 그룹의 한달 평균 배출량
        return get_object_or_404(Showerdataset, age=pk)

    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        logging.warn(user.age)
        Showerdataset = self.get_dataSet(user.age)
        serializer = ShowerdatasetSerializer(Showerdataset)
        return Response(serializer.data)

class PersonalShowerEmissionAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Personalshowerdata, user_id=pk)

    def get(self, request, pk, format=None): # 이번 월 1일 ~ 현재까지 내 배출량 합
        output = self.get_object(pk) 
        serializer = ShowerdatasetSerializer(output)
        return Response(serializer.data)
    
    def put(self, request, pk):
        output = self.get_object(pk)
        serializer = ShowerlogSerializer(output, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)