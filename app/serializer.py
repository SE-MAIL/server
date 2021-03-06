from rest_framework.serializers import ModelSerializer

from .models import Family, Personalshowerdata, Showerdataset
from .models import Showerlog

class PersonalShowerdataSerializer(ModelSerializer):
    class Meta:
        model = Personalshowerdata
        fields = ('__all__') #'__all__'

class ShowerdatasetSerializer(ModelSerializer):
    class Meta:
        model = Showerdataset
        fields = ('__all__')

class showerLogSumSerializer(ModelSerializer):
    class Meta:
        model = Showerlog
        fields = ('__all__')

class familySerializer(ModelSerializer):
    class Meta:
        model = Family
        fields = ('__all__')