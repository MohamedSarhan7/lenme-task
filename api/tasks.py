
from celery import shared_task
from .models import ScheduledPayments,LoanStatus

@shared_task
def transfer_money(scheduled_payment:ScheduledPayments):
  status=scheduled_payment.borrower.transfare_money(
    user=scheduled_payment.investor,
    amount=scheduled_payment.payment_amount)
  
  if status:
    scheduled_payment.is_paid=True
    scheduled_payment.save()
    
  
  if scheduled_payment.is_last_payment:
    scheduled_payment.loan.loan_status=LoanStatus.COMPLETED
    scheduled_payment.loan.save()
  