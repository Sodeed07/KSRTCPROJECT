from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Passenger
from .serializers import PassengerSerializer

@api_view(['GET'])
def test_api(request):
    return Response({"message": "BusBite backend is working!"})


@api_view(['POST'])
def register_passenger(request):
    serializer = PassengerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Passenger registered successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_passenger(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        passenger = Passenger.objects.get(email=email, password=password)
        serializer = PassengerSerializer(passenger)
        return Response({"message": "Login successful", "data": serializer.data}, status=status.HTTP_200_OK)
    except Passenger.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
