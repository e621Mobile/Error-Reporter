from django.contrib import admin
from error_report.models import *

admin.site.register(ReportTag)
admin.site.register(Message)
admin.site.register(Report)
admin.site.register(App)
admin.site.register(ErrorReportUser)
