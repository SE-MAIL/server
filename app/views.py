from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AuthUser, Family, Personalshowerdata, Showerdataset, Showerlog, Userinfo
from .serializer import ShowerdatasetSerializer, ShowerlogSerializer
import datetime, logging
from django.http import JsonResponse
from app import models
import random
from rest_framework.permissions import IsAuthenticated
import jwt
from rest_framework import status
from config.settings import SIMPLE_JWT


# Create your views here.

class SignupAPIView(APIView):
    def generateFID(self):
        id = random.randint(1, 999)
        return id

    def post(self, request):
        if not(request.data['id'] and request.data['pw'] and
         request.data['name'] and str(request.data['gender']) and
         request.data['age'] and str(request.data['isNew']) and request.data['familyID']):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        try:
            id = int(request.data['familyID'])
            if request.data['isNew']:
                id = int(self.generateFID())
                family = Family.objects.create(idfamily=id, familycap=request.data['familyCap'])
                family.save()
            family = Family.objects.get(idfamily=id)
            user = AuthUser.objects.create_user(username=request.data['id'], password=request.data['pw'], family_idfamily=family, first_name=request.data['name'])
            userInfo = models.Userinfo(auth_user=user, gender=request.data['gender'], age=request.data['age'])
            user.save()
            userInfo.save()
            return Response({"result": "OK"})
        except:
            return Response({"result": "FAIL"})

class ShowerdatasetEmissionAPIView(APIView):
    def get_user(self, pk):
        return get_object_or_404(AuthUser, username=pk)

    def get_dataSet(self, pk): # 해당 성별, 나이대 그룹의 한달 평균 배출량
        return get_object_or_404(Showerdataset, age=pk)

    def get_userInfo(self, pk):
            return get_object_or_404(Userinfo, auth_user_id=pk)

    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        userInfo = self.get_userInfo(user.id)
        logging.warn(userInfo.age)
        Showerdataset = self.get_dataSet(userInfo.age)
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

class ActionShowerStartAPIView(APIView): # 시작할 때 받는거
    def get(self, request, format=None): # 시작, 끝시간 체크
        time = datetime.timezone
        return Response(1)

    def post(self, request, format=None): # 시작, 끝시간 체크
        time = datetime.timezone
        response = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "shower": "샤워",
                "time" : "시작",
            }
        }
        return JsonResponse(response)

    
class ActionShowerEndAPIView(APIView): # 끝날 때 받는거, 누구에서 '나 샤워 끝났어' 액션을 하나 더 만들어서 여기에 연결
# 여기서 showerlog table의 endTime 기록 후 sum 처리
    def sumMonthlyEmission(self):
        latestLog = Showerlog.objects.fileter(id=id).last()
        startTime = latestLog.startTime
        endTime = latestLog.endTime
        emission = latestLog.emissions

        if startTime[0:6] != endTime[0:6] :
            latestLog.sum == 0
        latestLog.sum += emission

        return latestLog.save()


class TestAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        Bearer, jwt_token = token.split(" ")
        decoded = jwt.decode(jwt_token, SIMPLE_JWT['SIGNING_KEY'], algorithms = [SIMPLE_JWT['ALGORITHM']],)

        return Response(decoded)
        
        
