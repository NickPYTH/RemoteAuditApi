from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(AuditorCompany)
admin.site.register(Company)
admin.site.register(Document)
admin.site.register(EmployerDocument)
admin.site.register(Employer)
admin.site.register(DocumentStatus)
admin.site.register(Invites)

admin.site.site_header = "Admin panel"

