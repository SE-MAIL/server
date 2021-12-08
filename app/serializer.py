from rest_framework.serializers import ModelSerializer

from .models import Personalshowerdata, Showerdataset
from .models import Showerlog

class PersonalShowerlogSerializer(ModelSerializer):
    class Meta:
        model = Personalshowerdata
        fields = ('__all__') #'__all__'

class ShowerdatasetSerializer(ModelSerializer):
    class Meta:
        model = Showerdataset
        fields = ('idshowerdataset', 'gender', 'age', 'averageemissions')
