from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny

from django.db.models import Q

import requests
from .models import *
from .serializer import MoviesDataSerializer
import json
# Create your views here.

movies_url = 'http://www.omdbapi.com/?'
api_key = '27a7891b'

class MoviesSearchApi(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		data = request.data
		# ##print(data)
		context = {}
		data_context = {}
		response = {}
		response_data = {}
		try:
			title = data['title']
			context['title__icontains'] = title
		except :
			response_data['message'] = "title required "
			return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
		
		check = MoviesData.objects.filter(**context)
		if check.exists():
			serializer_data = MoviesDataSerializer(check,many=True)
			response_data['data'] = serializer_data.data
			response_data['message'] = 'title matching data exists in database'
			return Response(response_data)
		else:
			try:
				response = requests.get(movies_url, params={'t':title,'apikey':api_key})
			except :
				response_data['message'] = "Unable to call third party APIS. Please try again later "
				return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
			
			data = json.loads(response.content)
			print(data)
			if data['Response'] == 'True' :
				# print(data)
				print(data['imdbID'])
				data_context['id'] = data['imdbID']
				data_context['title'] = data['Title']
				data_context['rating'] = data['imdbRating']
				data_context['released_year'] = data['Year']
				data_context['genres'] = data['Genre']
				data = MoviesDataSerializer(data=data_context)
				if data.is_valid():
					data.save()
					response_data['data'] = data.data
					response_data['message'] = 'title matching data fetched from omdbapi and stored in database'
					return Response(response_data)
				else:
					return response(serializer.validated_data,status=status.HTTP_403_FORBIDDEN)
			else:
				response_data['message'] = data['Error']
				return Response(response_data,status=status.HTTP_404_NOT_FOUND)

class MoviesSearchApiInLocalDb(APIView):
	permission_classes = (AllowAny,)
	
	def post(self, request):
		data = request.data
		query_context = {}
		response_context = {}
		if 'title' in data:
			query_context['title__icontains'] = data['title']
		if 'genre' in data:
			query_context['genres__icontains'] = data['genres']

		if 'id' in data:
			query_context['id__iexact'] = data['id']

		if 'released_year' in data:
			query_context['released_year__iexact'] = data['released_year']

		if 'rating' in data:
			query_context['rating__gte'] = data['rating']

		print(query_context)
		check = MoviesData.objects.filter(**query_context)
		if check.exists():
			response_context['data'] = MoviesDataSerializer(check,many=True).data
			return Response(response_context,status=status.HTTP_200_OK)
		else:
			response_context['message'] = "data not found"
			return Response(response_context,status=status.HTTP_404_NOT_FOUND)
