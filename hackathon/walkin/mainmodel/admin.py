from django.contrib import admin

from mainmodel.models import Company, Freelancer, userlikes,Project
# Register your models here.
admin.site.register(Company)
admin.site.register(Freelancer)
admin.site.register(userlikes)
admin.site.register(Project)