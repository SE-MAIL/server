from django.contrib import admin
from .models import User
from .models import Showerdataset
from .models import Showerlog
from .models import Personalshowerdata
# Register your models here.
admin.site.register(User)
admin.site.register(Showerdataset)
admin.site.register(Showerlog)
admin.site.register(Personalshowerdata)