from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here

class Family(models.Model):
    idfamily = models.IntegerField(db_column='idFamily', primary_key=True)  # Field name made lowercase.
    familycap = models.CharField(db_column='familyCap', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Family'

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not id:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)
class AuthUser(AbstractBaseUser):
    objects = UserManager()
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=254, blank=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    family_idfamily = models.ForeignKey(Family, models.DO_NOTHING, db_column='Family_idFamily')  # Field name made lowercase.
    USERNAME_FIELD = "username"
    class Meta:
        managed = False
        db_table = 'auth_user'


class Showerdataset(models.Model):
    idshowerdataset = models.IntegerField(db_column='idshowerDataSet', primary_key=True)  # Field name made lowercase.
    gender = models.IntegerField(blank=True, null=True)
    age = models.CharField(max_length=45, blank=True, null=True)
    averageemissions = models.IntegerField(db_column='averageEmissions', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'showerDataSet'
        
class Personalshowerdata(models.Model):
    idcurrentshowerdata = models.AutoField(db_column='idcurrentShowerData', primary_key=True)  # Field name made lowercase.
    targettime = models.IntegerField(db_column='targetTime', blank=True, null=True)  # Field name made lowercase.
    reduction = models.IntegerField(blank=True, null=True)
    auth_user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Personalshowerdata'

class Showerlog(models.Model):
    idshower = models.AutoField(primary_key=True)
    starttime = models.DateTimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    takentime = models.IntegerField(db_column='takenTime', blank=True, null=True)  # Field name made lowercase.
    emissions = models.IntegerField(blank=True, null=True)
    sum = models.IntegerField(blank=True, null=True)
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'showerLog'

class Userinfo(models.Model):
    auth_user = models.OneToOneField('AuthUser', models.DO_NOTHING, primary_key=True)
    gender = models.IntegerField(blank=True, null=True)
    age = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UserInfo'

