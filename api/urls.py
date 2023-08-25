from django.urls import path,include
from .views import register,LoanList,OfferList,OfferDetails,GetOffersbyLoan
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # authentication
    path('auth/register', register),
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # loan
    path('loans', LoanList.as_view()),
    path('offers', OfferList.as_view()),
    path('offers/<int:id>', OfferDetails.as_view()),
    path('loans/<int:id>/offers', GetOffersbyLoan.as_view())
]