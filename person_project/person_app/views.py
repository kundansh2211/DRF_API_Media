from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Person
from .serializers import PersonSerializer
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail


class PersonAPIView(APIView):
    def get(self, request, pk=None):
        if pk == None:
            queryset = Person.objects.all()
            serializer = PersonSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        else:
            obj = get_object_or_404(Person, pk=pk)
            serializer= PersonSerializer(obj)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        return Response("Invalid pk", status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            subject = 'Registration Successfull'
            message = 'Thank You for Registering with us, Enjoy the application!'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [user.email])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        obj = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(data=request.data, instance=obj)
        if serializer.is_valid():
            serializer.save()
            subject = 'Update Successfull'
            message = 'Your Credentials have been updated successfully'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [obj.email])
            return Response(data=serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        obj = get_object_or_404(Person,pk=pk)
        serializer = PersonSerializer(data=request.data, instance=obj, partial = True)
        if serializer.is_valid():
            serializer.save()
            subject = 'Update Successfull'
            message = 'Your Credentials have been updated successfully'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [obj.email])
            return Response(data=serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        obj = get_object_or_404(Person, pk=pk)
        subject = 'Deleted Successfull'
        message = 'Sorry to see You going'
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, [obj.email])
        obj.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

