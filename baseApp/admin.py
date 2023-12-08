from django.contrib import admin
from .models import Member, Contribution, Managers, ApplyLoanRequest, Payment, Message
# Register your models here.

admin.site.register(Member)
admin.site.register(Contribution)
admin.site.register(Managers)
admin.site.register(ApplyLoanRequest)
admin.site.register(Payment)
admin.site.register(Message)



