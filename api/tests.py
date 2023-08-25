from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Loan,CustomUser,UserType,Offer
from .serializers import LoanSerializer,OfferSerializer


class LoanListTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('loan-list')
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword',type=UserType.BORRWOER)
        self.client.force_authenticate(user=self.user)

    def test_get_loan_list(self):
        loan1 = Loan.objects.create(borrower=self.user, loan_amount=1000,loan_period=4)
        # loan2 = Loan.objects.create(borrower=self.user, loan_amount=2000,loan_period=4)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = LoanSerializer([loan1], many=True).data
        self.assertEqual(response.data['results'], expected_data)

    def test_create_loan(self):
        data = {
            'loan_amount': 1500,
            'loan_period': 15
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loan = Loan.objects.get(pk=response.data['id'])
        self.assertEqual(loan.borrower, self.user)
        self.assertEqual(loan.loan_amount, data['loan_amount'])
        self.assertEqual(loan.loan_period, data['loan_period'])

class OfferListTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('offer-list')

        self.user = CustomUser.objects.create_user(username='testuser1', password='testpassword',type=UserType.INVESTOR,balance=500000)
        self.borrower = CustomUser.objects.create_user(username='testuser2', password='testpassword',type=UserType.BORRWOER)
        self.client.force_authenticate(user=self.user)

        self.loan = Loan.objects.create(borrower=self.borrower, loan_amount=1000,loan_period=4)

        self.offer1 = Offer.objects.create(investor=self.user,loan=self.loan, annual_interest_rate=5)
        # self.offer2 = Offer.objects.create(investor=self.user,loan=self.loan, annual_interest_rate=10)

    def test_get_offer_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = OfferSerializer([self.offer1], many=True).data
        self.assertEqual(response.data['results'], expected_data)

    def test_create_offer(self):
        data = {
            'loan': self.loan.id,
            'annual_interest_rate': 15
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        offer = Offer.objects.get(pk=response.data['id'])
        self.assertEqual(offer.investor, self.user)
        self.assertEqual(offer.loan, self.loan)
        self.assertEqual(offer.annual_interest_rate, data['annual_interest_rate'])
        
class GetOffersbyLoanTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('offers-by-loan', args=[1])
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword',type=UserType.INVESTOR,balance=500000)
        self.borrower = CustomUser.objects.create_user(username='testuser2', password='testpassword',type=UserType.BORRWOER)

        self.client.force_authenticate(user=self.user)

        self.loan = Loan.objects.create(borrower=self.user, loan_amount=1000,loan_period=4)

        self.offer1 = Offer.objects.create(investor=self.user,loan=self.loan, annual_interest_rate=5)
        # self.offer2 = Offer.objects.create(investor=self.user,loan=self.loan, annual_interest_rate=10)

    def test_get_offers_by_loan(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = OfferSerializer([self.offer1], many=True).data
        self.assertEqual(response.data['results'], expected_data)
