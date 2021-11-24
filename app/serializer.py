from rest_framework.serializers import ModelSerializer

from .models import Showerdataset
from .models import Showerlog

class ShowerlogSerializer(ModelSerializer):
    class Meta:
        model = Showerlog
        fields = ('idshower', 'startTime', 'endTime', 'takenTime', 'data', 'user_id', 'emissions') #'__all__'

class ShowerdatasetSerializer(ModelSerializer):
    class Meta:
        model = Showerdataset
        fields = ('idshowerdataset', 'gender', 'age', 'averageemissions', 'count')