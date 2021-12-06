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
import datetime
from django.utils import timezone
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
    def getUser(self, first_name):
        return get_object_or_404(AuthUser, first_name=first_name)

    def post(self, request, format=None): # 시작, 끝시간 체크
        try:
            starttime = timezone.now()+datetime.timedelta(hours=9)
            first_name = request.data['action']['parameters']['user']['value']
            user = self.getUser(first_name)
            latestLog = Showerlog.objects.filter(auth_user=user).last()
            showerlog = models.Showerlog(auth_user=user, starttime=starttime, sum=latestLog.sum)
            showerlog.save()

            response = {
                "version": "2.0",
                "resultCode": "OK",
                "output": {
                    "user": "{first_name}",
                }
            }
            return JsonResponse(response)
        except:
            return JsonResponse({
                "version": "2.0",
                "resultCode": "error",
                }
            )

    
class ActionShowerEndAPIView(APIView): # 끝날 때 받는거, 누구에서 '나 샤워 끝났어' 액션을 하나 더 만들어서 여기에 연결
# 여기서 showerlog table의 endTime 기록 후 sum 처리
    def getUser(self, first_name):
        return get_object_or_404(AuthUser, first_name=first_name)

    def post(self, request, format=None):
        try:
            endTime = timezone.now()+datetime.timedelta(hours=9)
            first_name = request.data['action']['parameters']['user']['value']
            user = self.getUser(first_name)

            showerLogList = Showerlog.objects.all().filter(auth_user=user)
            latestLog = showerLogList.last()
            logging.warn(latestLog)
            beforeLastestLog = showerLogList.order_by('-idshower')[1]
            logging.warn(beforeLastestLog)

            startTime = latestLog.starttime
            takenTime = (endTime - startTime).total_seconds()
            latestLog.takentime = takenTime
            emissions = takenTime*2
            latestLog.emissions = emissions
            if str(beforeLastestLog.starttime)[0:7] != str(endTime)[0:7] :
                logging.warn(str(beforeLastestLog.starttime)[0:7])
                logging.warn(str(endTime)[0:7])
                latestLog.sum == 0
            latestLog.sum = latestLog.sum + emissions
            latestLog.endtime=endTime
            latestLog.save()
            response = {
                    "version": "2.0",
                    "resultCode": "OK",
                    "output": {
                        "user": "{first_name}",
                    }
                }
            return JsonResponse(response)
        except:
            return JsonResponse({
                "version": "2.0",
                "resultCode": "error",
                }
            )


class TestAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        Bearer, jwt_token = token.split(" ")
        decoded = jwt.decode(jwt_token, SIMPLE_JWT['SIGNING_KEY'], algorithms = [SIMPLE_JWT['ALGORITHM']],)

        return Response(decoded)
        
        
