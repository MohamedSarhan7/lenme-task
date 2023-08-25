from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import RegisterSerializer,LoanSerializer
from .models import Loan
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
        serializer = LoanSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)

