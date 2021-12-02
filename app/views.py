from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Personalshowerdata, Showerdataset, User, Showerlog
from .serializer import ShowerdatasetSerializer, ShowerlogSerializer
import datetime, logging
from django.http import JsonResponse
# Create your views here.

class UserAPIView(APIView):
    def signup(request): # 회원 가입
        if request.method == 'POST': #signup 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
            if request.POST['password'] == request.POST['confirm']: # password와 confirm에 입력된 값이 같다면
                user = User.objects.create_user(userID=request.POST['userID'], pw=request.POST['password'], name=request.POST['name'], age=request.POST['age'], gender=request.POST['gender']) # user 객체를 새로 생성
            elif request.POST['userID']: # 회원 가입 때 id가 입력된다면 : 가구원 등록
                user = User.objects.create_user(userID=request.POST['userID'], pw=request.POST['password'], name=request.POST['name'], age=request.POST['age'], gender=request.POST['gender']) # user 객체를 새로 생성
            auth.login(request, user) # 로그인 한다
            return redirect('/')
        return render(request, 'signup.html')  # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다.

    def login(request): # 로그인
        if request.method == 'POST': # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
            userID = request.POST['userID'] # login.html에서 넘어온 username과 
            password = request.POST['password'] # password를 각 변수에 저장한다.

            user = auth.authenticate(request, userID=userID, password=password)  # 해당 username과 password와 일치하는 user 객체를 가져온다.
        
            if user is not None: # 해당 user 객체가 존재한다면
                auth.login(request, user) # 로그인 한다
                return redirect('/')
            else: # 존재하지 않는다면
                return render(request, 'login.html', {'error' : 'id or password is incorrect.'})  # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
        else:  # login으로 GET 요청이 들어왔을때, 로그인 화면을 띄워준다.
            return render(request, 'login.html')

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

    
        
        
