from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from datetime import datetime
from . import models, serializers



class SignUpView(APIView):

	def post(self, request):
		serializer = serializers.SignUpSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientView(APIView):

	def get(self, request):
		clients = models.Client.objects.all()
		serializer = serializers.ClientSerializer(clients, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = serializers.ClientSerializerPost(data=request.data)
		if serializer.is_valid():
			sales_contact = get_object_or_404(models.User, pk=int(request.data['sales_contact_id']))
			serializer.save(sales_contact_id=sales_contact)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientViewDetail(APIView):

	def get(self, request, client_id):
		client = get_object_or_404(models.Client, pk=client_id)
		serializer = serializers.ClientSerializer(client)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def put(self, request, client_id):
		client = get_object_or_404(models.Client, pk=client_id)
		serializer = serializers.ClientSerializerPost(client, data=request.data)
		if serializer.is_valid():
			serializer.save(date_updated=datetime.now().isoformat())
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, client_id):
		client = get_object_or_404(models.Client, pk=client_id)
		client.delete()
		return Response(status=status.HTTP_200_OK)



