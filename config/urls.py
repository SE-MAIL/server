from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recommended/shower/personaldata/<pk>/', views.PersonalShowerEmissionAPIView.as_view()),
    path('recommended/shower/dataset/<pk>/', views.ShowerdatasetEmissionAPIView.as_view()),
    path('answer.shower', views.ActionShowerStartAPIView.as_view()),
    # 누구는 http://www.~~~.com/answer.shower  이 주소로 요청을 보냈는데
    # 장고에서는 /answer.shower 에 해당하는 주소가 없어서 마음대로 /를 붙여준겨!
    # 그리고 나서 보니까 /answer.shower/가 리스트에 존재하니까 /answer.shower/로 리다이렉트해줌.
    # 이때 리다이렉트 해주는 과정에서 오류가 발생하는 것이엇음
    # 해결책은 애초에 path를 등록할 때 마지막 /를 떼주면
    # 누구가 처음 요청을 보낼 때 한 번에 연결이 가능함.
]
