from django.db import models

# Create your models here.
class Personalshowerdata(models.Model):
    idcurrentshowerdata = models.IntegerField(db_column='idcurrentShowerData', primary_key=True)  # Field name made lowercase.
    targettime = models.IntegerField(db_column='targetTime', blank=True, null=True)  # Field name made lowercase.
    reduction = models.IntegerField(db_column='reduction', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Personalshowerdata'


class Showerdataset(models.Model):
    idshowerdataset = models.IntegerField(db_column='idshowerDataSet', primary_key=True)  # Field name made lowercase.
    gender = models.IntegerField(blank=True, null=True)
    age = models.CharField(max_length=45, blank=True, null=True)
    averageemissions = models.IntegerField(db_column='averageEmissions', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'showerDataSet'


class Showerlog(models.Model):
    idshower = models.IntegerField(primary_key=True)
    starttime = models.DateTimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    takentime = models.IntegerField(db_column='takenTime', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    emissions = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'showerLog'


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    pw = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=45, blank=True, null=True)
    age = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'