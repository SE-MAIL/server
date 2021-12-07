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
    # 가입할 때 받는 값들
    # id pw name gender age - 기본 유저 데이터
    # isNew - 새로운 가구를 만들면 1, 기존 가구에 참여는 0
    # familyID - 새로운 가구 생성시 임의의 양의 정수 넣어서 보냄, 기존 가구 참여시 해당 가구 ID, familyID는 1부터 999까지 양의 정수
    # familyCap - 새로운 가구 생성시 해당 가구원 수, 기존가구 참여시 임의의 양의 정수.

    def generateFID(self):
        id = random.randint(1, 999)
        # 랜덤인트 돌렸을 때 이미 있는 값인지.
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
        return get_object_or_404(AuthUser, first_name=first_name) # AuthUser가 User 테이블, first_name은 사용자의 이름

    def post(self, request, format=None): # 시작, 끝시간 체크
        # try:
            starttime = timezone.now()+datetime.timedelta(hours=9)
            first_name = request.data['action']['parameters']['user']['value'] # 누구의 요청에서 사용자의 이름 받기
            user = self.getUser(first_name) # 사용자 이름으로 user 테이블에서 해당 사용자 데이터 불러오기
            latestLog = Showerlog.objects.filter(auth_user=user).last() # 유저 데이터로 샤워로그 테이블 조회
            showerlog = models.Showerlog(auth_user=user, starttime=starttime, sum=latestLog.sum) # sum은 직전 값을 불러옴.
            personalData = Personalshowerdata.objects.get(auth_user = user)
            targetMinute = int(personalData.targettime / 60)
            targetSecond = int(personalData.targettime % 60)
            showerlog.save()

            response = {
                "version": "2.0",
                "resultCode": "OK",
                "output": {
                    "user": f"{first_name}",
                    "target_minute" : f"{targetMinute}",
                    "target_second" : f"{targetSecond}",
                }
            }
            return JsonResponse(response)
        # except:
        #     return JsonResponse({
        #         "version": "2.0",
        #         "resultCode": "error",
        #         }
        #     )

    
class ActionShowerEndAPIView(APIView): # 끝날 때 받는거, 누구에서 '나 샤워 끝났어' 액션을 하나 더 만들어서 여기에 연결
# 여기서 showerlog table의 endTime 기록 후 sum 처리
    def getUser(self, first_name):
        return get_object_or_404(AuthUser, first_name=first_name)

    def post(self, request, format=None):
        # try:
            endTime = timezone.now()+datetime.timedelta(hours=9) # 요청 들어왔을 때 시간 기록
            first_name = request.data['action']['parameters']['user']['value'] # 샤워시작과 동일 - 유저 데이터 불러오기
            user = self.getUser(first_name) # 샤워시작과 동일

            personalData = Personalshowerdata.objects.get(auth_user = user)
            showerLogList = Showerlog.objects.all().filter(auth_user=user) # 유저 데이터로 샤워로그 기록 조회. 해당 유저의 샤워로그 전체를 불러옴.
            latestLog = showerLogList.last() # 해당 유저의 전체 로그 중 마지막
            firstLog = showerLogList.first()
            beforeLastestLog = showerLogList.order_by('-idshower')[1] # 해당 유저의 전체 로그 중 마지막에서 두번째 값.
            # order_by('조건')에서 조건 앞에 -를 붙이면 역순으로 정렬함(내림차순). -> [0]번이 가장 마지막 값(==last()) [1]이 마지막에서 두 번째 값.

            startTime = latestLog.starttime # 가장 마지막 로그에서 시작시간 불러옴.
            takenTime = (endTime - startTime).total_seconds() # 종료시간 - 시작시간 = 총 소요시간
            # total_seconds()는 datetime type을 초 단위로 변환해줌.
            latestLog.takentime = takenTime # 가장 마지막 로그에 소요시간 저장
            emissions = takenTime*2 # 샤워 10분당 1080g의 탄소배출 -> 1초당 약 1.8g 배출 => 약 2g배출로 계산.

            latestLog.emissions = emissions # 배출량 저장.
            if str(beforeLastestLog.starttime)[0:7] != str(endTime)[0:7] : # 마지막에서 두번째값의 일자와 현재 일자를 비교
                # latestLog(가장 마지막 row)는 현재 샤워를 시작했을 때 기록된 row다. 따라서 이전 샤워 데이터를 불러오려면 마지막에서 두 번째 값을 불러와야 함.
                latestLog.sum == 0
            latestLog.sum = latestLog.sum + emissions
            latestLog.endtime=endTime
            is_success = 'success'
            if takenTime > personalData.targettime:
                is_success = 'fail'
            reductionTime = int(personalData.targettime - takenTime)
            if reductionTime < 0:
                reductionTime = 0
            reduction_carbon = int((firstLog.takentime - takenTime) * 2)
            emission_carbon = int(emissions)
            latestLog.save()
            response = {
                    "version": "2.0",
                    "resultCode": "OK",
                    "output": {
                        "showerEndUser": f"{first_name}",
                        "is_success": f"{is_success}",
                        "emission_carbon": f"{emission_carbon}",
                        "reduction_time": f"{reductionTime}",
                        "reduction_carbon": f"{reduction_carbon}"

                    }
                }
            return JsonResponse(response)
        # except:
        #     return JsonResponse({
        #         "version": "2.0",
        #         "resultCode": "error",
        #         }
        #     )


class TestAPIView(APIView): # 로그인 기능 토큰 확인용 테스트 뷰
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        Bearer, jwt_token = token.split(" ")
        decoded = jwt.decode(jwt_token, SIMPLE_JWT['SIGNING_KEY'], algorithms = [SIMPLE_JWT['ALGORITHM']],)

        return Response(decoded)
        
        
