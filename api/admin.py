from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

UserAdmin.fieldsets +=(
  ('Extra Fields', {'fields': ('type','balance' )}),
)

class LoanAdmin(admin.ModelAdmin):
  list_display =['borrower','total_loan_amount','loan_amount_after_annual_interest_rate','loan_amount','loan_period','lenme_fee','loan_status']
  readonly_fields=('loan_amount_after_annual_interest_rate',)
  
class ScheduledPaymentsAdmin(admin.ModelAdmin):
  list_display=['borrower','investor','payment_amount','payment_date','is_last_payment']
admin.site.register(CustomUser,UserAdmin)
admin.site.register(Loan,LoanAdmin)
admin.site.register(Offer)
admin.site.register(ScheduledPayments,ScheduledPaymentsAdmin)