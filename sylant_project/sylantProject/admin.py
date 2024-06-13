from django.contrib import admin
from .models import CustomUser, Machine, Maintenance, Claim, Reference, ReferenceEntity

admin.site.register(CustomUser)
admin.site.register(Machine)
admin.site.register(Maintenance)
admin.site.register(Claim)
admin.site.register(Reference)
admin.site.register(ReferenceEntity)
