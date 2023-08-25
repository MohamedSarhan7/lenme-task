from datetime import timedelta,date
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
# Create your models here.

class UserType(models.TextChoices):
    BORRWOER = "BORRWOER"
    INVESTOR = "INVESTOR"
    
class LoanStatus(models.TextChoices):
    FUNDED = "FUNDED"
    PENDING = "PENDING"
    COMPLETED ="COMPLETED"

class CustomUser(AbstractUser):
  type = models.CharField(max_length=250,choices=UserType.choices,default=UserType.BORRWOER)
  balance = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
  
  def check_balance(self,amount):
      return self.balance >= amount
  
  def transfer_money(self,user,amount):
    if self.check_balance(amount):
      self.balance -= amount
      user.balance +=amount
      self.save()
      user.save()
      return True
    return False  

class Loan(models.Model):
  

        
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="borrower_loans")
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_amount_after_annual_interest_rate= models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    loan_period = models.PositiveIntegerField(help_text="in months")
    loan_status = models.CharField(max_length=20, choices=LoanStatus.choices, default=LoanStatus.PENDING)
    lenme_fee=models.DecimalField(max_digits=10, decimal_places=2, default=3.00)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    @property
    def total_loan_amount(self):
      # pass
      return self.loan_amount_after_annual_interest_rate+self.lenme_fee
    
    
    def __str__(self):
      return self.borrower.username
    
    def calc_loan_amount_after_annual_interest_rate(self,rate):
      self.loan_amount_after_annual_interest_rate = self.loan_amount+(self.loan_amount*(rate/100))
      self.save()
      
    def create_scheduled_payments(self,investor):
      amount=self.total_loan_amount/self.loan_period
      months=self.get_next_n_months_dates_from_next_month(self.loan_period)
      
      scheduled_payments = []
      for index,date in enumerate(months):
        scheduled_payment = ScheduledPayments(
          borrower=self.borrower,
          investor=investor,
          payment_amount=amount,
          payment_date=date,
          loan=self
          )
        if index == len(months)-1:
          scheduled_payment.is_last_payment=True
        scheduled_payments.append(scheduled_payment)
      ScheduledPayments.objects.bulk_create(scheduled_payments)
    
    def get_next_n_months_dates_from_next_month(self,n):
      today = datetime.date.today()
      next_month = today + relativedelta(months=1)
      next_n_months_dates = [next_month + relativedelta(months=i) for i in range(n)]
      return next_n_months_dates
    
class Offer(models.Model):
  investor=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
  loan=models.ForeignKey(Loan, on_delete=models.CASCADE,related_name='offers')
  annual_interest_rate=models.DecimalField(max_digits=10,decimal_places=2,default=0.00,help_text="out of 100% ")
  is_accepted=models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  
  class Meta:
        ordering = ["-created_at"]
  
  def __str__(self) -> str:
    return self.investor.username
  
  def save(self, *args, **kwargs):
    """Create scheduled payments and recalculate the loan total amount if offer accepted"""
    if self.is_accepted:
      
      self.loan.loan_status = LoanStatus.FUNDED
      self.loan.calc_loan_amount_after_annual_interest_rate(self.annual_interest_rate)
      self.loan.save()
      
      self.loan.create_scheduled_payments(self.investor)
      self.investor.transfer_money(self.loan.borrower, self.loan.loan_amount)
      super().save(*args, **kwargs)
        
    else:
      super().save(*args, **kwargs)
    

  

  
class ScheduledPayments(models.Model):
  borrower=models.ForeignKey(CustomUser, on_delete=models.Case,related_name="borrower_payments")
  investor=models.ForeignKey(CustomUser, on_delete=models.Case)
  loan=models.ForeignKey(Loan, on_delete=models.CASCADE)
  payment_amount=models.DecimalField(max_digits=10,decimal_places=2)
  payment_date=models.DateField()
  is_paid = models.BooleanField(default=False)
  is_last_payment = models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  
  def __str__(self) -> str:
    return self.borrower.username