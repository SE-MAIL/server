from rest_framework.serializers import ModelSerializer

from .models import Showerdataset
from .models import Showerlog

class ShowerlogSerializer(ModelSerializer):
    class Meta:
        model = Showerlog
        fields = ('idshower', 'starttime', 'endtime', 'takentime', 'user_id', 'emissions', 'sum') #'__all__'

class ShowerdatasetSerializer(ModelSerializer):
    class Meta:
        model = Showerdataset
        fields = ('idshowerdataset', 'gender', 'age', 'averageemissions')
