from django.contrib import admin
from .models import AuthUser, Family, Showerdataset, Showerlog, Personalshowerdata, Userinfo
# Register your models here.
admin.site.register(AuthUser)
admin.site.register(Showerdataset)
admin.site.register(Showerlog)
admin.site.register(Personalshowerdata)
admin.site.register(Userinfo)
admin.site.register(Family)

