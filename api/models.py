from datetime import timedelta,date
from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
# Create your models here.

class UserType(Enum):
  BORRWOER = "BORRWOER"
  INVESTOR = "INVESTOR"

class LoanStatus(Enum):
  FUNDED = "FUNDED"
  PENDING = "PENDING"
  COMPLETED ="COMPLETED"
  
class CustomUser(AbstractUser):
  type = models.CharField(max_length=250,choices=UserType.choices)
  balance = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
  
# class Borrower(models.Model):
#     user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="type")

# class Investor(models.Model):
#     user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="type")

class Loan(models.Model):
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    investor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_period = models.PositiveIntegerField(help_text="in months")
    annual_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_status = models.CharField(max_length=20, choices=LoanStatus.choices, default=LoanStatus.PENDING)
    lenme_fee=models.DecimalField(max_digits=10, decimal_places=2, default=3.00)
    loan_endtime = models.DateField(default=(date.today() + timedelta(weeks=(loan_period*4))))
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    @property
    def total_loan_amount(self):
      return self.loan_amount+self.lenme_fee
      
    def __str__(self):
      return self.borrower.username
    
class Offer(models.Model):
  investor=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
  loan=models.ForeignKey(Loan, on_delete=models.CASCADE)
  annual_interest_rate=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
  is_accepted=models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  
  def __str__(self) -> str:
    return self.investor.username
  
class ScheduedPayments(models.Model):
  borrower=models.ForeignKey(CustomUser, on_delete=models.Case)
  investor=models.ForeignKey(CustomUser, on_delete=models.Case)
  payment_amount=models.DecimalField(max_digits=10,decimal_places=2)
  payment_data=models.DateField()
  is_paid = models.BooleanField(default=False)
  is_last_payment = models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  
  def __str__(self) -> str:
    return self.borrower.username