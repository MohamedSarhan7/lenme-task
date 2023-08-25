from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import Http404

from .serializers import RegisterSerializer,LoanSerializer,OfferSerializer,ScheduledPaymentsSerializer
from .models import Loan,Offer,ScheduledPayments
# Create your views here.

@api_view([ 'POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        return Response(
            {
                "user":serializer.data,
                },
            status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanList(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    pagination_class = PageNumberPagination
    
    def get(self, request):
        # loans= Loan.objects.get()
        paginator=self.pagination_class()
        result= paginator.paginate_queryset(queryset=Loan.objects.all(),request=request)
        serializer= LoanSerializer(result,many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self,request):
        data = request.data.copy()
        data['borrower'] = request.user.id
        if request.user.type!= "BORROWER":
            return Response(data={"error":"not allowed"},status=status.HTTP_403_FORBIDDEN)
        serializer = LoanSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)



class OfferList(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    pagination_class = PageNumberPagination
    
    def get(self, request):
        paginator=self.pagination_class()
        result= paginator.paginate_queryset(queryset=Offer.objects.all(),request=request)
        serializer= OfferSerializer(result,many=True)
        return paginator.get_paginated_response(serializer.data)
        
    def post(self, request):
        data = request.data.copy()
        data['investor'] = request.user.id
        if request.user.type!= "INVESTOR":
            return Response(data={"error":"not allowed"},status=status.HTTP_403_FORBIDDEN)
        # loan=get_object_or_404(Loan,pk=data['loan'])
        serializer = OfferSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)


class OfferDetails(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def put(self, request,id):
        try:
            offer=get_object_or_404(Offer,id=id)
            is_accepted= self.request.query_params.get('is_accepted')
            if not is_accepted:
                return Response(data={"error":"is_accepted not provided in query params"},status=status.HTTP_400_BAD_REQUEST)    
            if is_accepted == "True" or is_accepted == True :
                if not offer.is_accepted:
                    offer.is_accepted=True
                    offer.save()
                    scheduled_payments= ScheduledPayments.objects.filter(loan=offer.loan)
                    serializer= ScheduledPaymentsSerializer(scheduled_payments,many=True)
                    return Response(data=serializer.data)
            
            return Response({"error":"is_accepted not valid "},status=status.HTTP_400_BAD_REQUEST)    
                
        except Http404:
            return Response(data={'error':'not found'},status=status.HTTP_404_NOT_FOUND)
        
# get offers by loan
class GetOffersbyLoan(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    pagination_class = PageNumberPagination
    
    def get(self, request,id):
        paginator=self.pagination_class()
        result= paginator.paginate_queryset(queryset=Offer.objects.filter(loan=id),request=request)
        serializer= OfferSerializer(result,many=True)
        return paginator.get_paginated_response(serializer.data)