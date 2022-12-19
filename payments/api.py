from .models import PaymentUser1, PaymentUser2, ExpiredPayments
from rest_framework import viewsets
from rest_framework import filters
from .serializer import PaymentSerializer1, PaymentSerializerAdmin, PaymentSerializerUser, PaymentExpiratedSerializer
from .pagination import StandardResultsSetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.settings import api_settings

class PaymentViewSet1(viewsets.ModelViewSet):
    queryset = PaymentUser1.objects.all()
    serializer_class = PaymentSerializer1
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    search_fields = ['user', 'paymentDate', 'name_service']
    throttle_scope = 'payment_1'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class PaymentUserViewSet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    pagination_class = StandardResultsSetPagination
    throttle_scope = 'payments'

    def get(self, request):
        payments = PaymentUser2.objects.all()
        serializer = PaymentSerializerUser(payments, many = True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        payment = PaymentSerializerUser(data=request.data)
         
        if payment.is_valid():
            payment.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(payment.errors, status=status.HTTP_400_BAD_REQUEST)
        



class PaymentAdminViewSet(viewsets.ModelViewSet):
    queryset = PaymentUser2.objects.all()
    serializer_class = PaymentSerializerAdmin
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    search_fields = ['paymentDate', 'expirationDate']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    
class PaymentExpiratedViewSet(viewsets.ModelViewSet):
    queryset = ExpiredPayments.objects.all()
    serializer_class = PaymentExpiratedSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)