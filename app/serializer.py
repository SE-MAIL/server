from rest_framework import serializers

from .models import Showerdataset
from .models import Showerlog

class ShowerlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showerlog
        fields = ('idshower', 'startTime', 'endTime', 'takenTime', 'data', 'user_id', 'emissions')

class ShowerdatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showerdataset
        fields = ('idshowerdataset', 'gender', 'age', 'averageemissions', 'count')
