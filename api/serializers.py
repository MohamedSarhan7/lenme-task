from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import CustomUser,Loan

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'first_name', 'last_name','type')
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)
    
    
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Loan
        fields=[
            'id',
            'borrower',
            'loan_amount',
            'loan_amount_after_annual_interest_rate',
            'total_loan_amount',
            'loan_period',
            'loan_status',
            'lenme_fee',
            'created_at',
            'updated_at'
            ]
        read_only_fields =('loan_status', 'loan_amount_after_annual_interest_rate', 'total_loan_amount',)