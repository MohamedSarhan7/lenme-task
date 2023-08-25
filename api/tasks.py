
from celery import shared_task
from .models import ScheduledPayments,LoanStatus
from django.db import transaction

@shared_task
def transfer_money(scheduled_payment:ScheduledPayments):
  with transaction.atomic():
    status=scheduled_payment.borrower.transfer_money(
      user=scheduled_payment.investor,
      amount=scheduled_payment.payment_amount)
    
    if status:
      scheduled_payment.is_paid=True
      scheduled_payment.save()
    else:
      return False

    if scheduled_payment.is_last_payment:
      scheduled_payment.loan.loan_status=LoanStatus.COMPLETED
      scheduled_payment.loan.save()

    return True
  