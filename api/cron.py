from api.tasks import transfer_money
from datetime import date
from .models import ScheduledPayments
def my_cron_job():
    scheduled_payments_list=ScheduledPayments.objects.filter(payment_date=date.today)
    for obj in scheduled_payments_list :
        transfer_money.delay(obj)