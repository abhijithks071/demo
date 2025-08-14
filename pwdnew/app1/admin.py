from django.contrib import admin

from .models import *
admin.site.register(user_reg)
admin.site.register(auth_reg)
admin.site.register(Complaint)
admin.site.register(ProgressReport)

# Register your models here.
