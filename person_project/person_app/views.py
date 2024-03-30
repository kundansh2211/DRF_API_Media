from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Person
from .serializers import PersonSerializer
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail
import logging


logger = logging.getLogger(__name__)


class PersonAPIView(APIView):
    def get(self, request, pk=None):
        try:
            if pk == None:
                queryset = Person.objects.all()
                serializer = PersonSerializer(queryset, many=True)
                logger.info(f'GET request for listing all users handled successfully')
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            
            else:
                obj = get_object_or_404(Person, pk=pk)
                serializer= PersonSerializer(obj)
                logger.info(f'GET request for user with id {pk} has been handled successfully')
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'An error occurred while handling GET request: {str(e)}', exc_info=True)
            return Response(data={'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def post(self, request):
        try:
            serializer = PersonSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                subject = 'Registration Successfull'
                message = 'Thank You for Registering with us, Enjoy the application!'
                email_from = settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from, [user.email])
                logger.info('User created successfully' )
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f'An error occurred while handling POST request: {str(e)}', exc_info=True)
            return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        try:
            obj = get_object_or_404(Person, pk=pk)
            serializer = PersonSerializer(data=request.data, instance=obj)
            if serializer.is_valid():
                serializer.save()
                subject = 'Update Successfull'
                message = 'Your Credentials have been updated successfully'
                email_from = settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from, [obj.email])
                logger.info('PUT request handled successfully')
                return Response(data=serializer.data, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f'An error occurred while handling PUT request: {str(e)}', exc_info=True)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        try:
            obj = get_object_or_404(Person,pk=pk)
            serializer = PersonSerializer(data=request.data, instance=obj, partial = True)
            if serializer.is_valid():
                serializer.save()
                subject = 'Update Successfull'
                message = 'Your Credentials have been updated successfully'
                email_from = settings.EMAIL_HOST_USER
                logger.info('PATCH request handled successfully')
                send_mail(subject, message, email_from, [obj.email])
                return Response(data=serializer.data, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f'An error occurred while handling PATCH request: {str(e)}', exc_info=True)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            obj = get_object_or_404(Person, pk=pk)
            subject = 'Deleted Successfull'
            message = 'Sorry to see You going'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [obj.email])
            obj.delete()
            logger.info('PUT request handled successfully')
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'An error occurred while handling DELETE request: {str(e)}', exc_info=True)
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
        

