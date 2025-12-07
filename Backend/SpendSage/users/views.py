from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import User
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from common.utils import api_success_response, api_error_response
from rest_framework.permissions import IsAuthenticated

# login and obtain token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Public endpoint for new user registration.
    generics.CreateAPIView becuase we don't need need other methods
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    
class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            return api_success_response("User registration successful", user, status.HTTP_201_CREATED)
        
        return api_error_response("User registration failed", serializer.errors, status.HTTP_400_BAD_REQUEST)   

class UserProfileView(APIView):
    """
    Protected endpoint to view and update the logged-in user's profile.
    Requires a valid JWT token.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retrieves the current user's details."""
        serializer = UserSerializer(request.user)
        return api_success_response("User details retrieved successfully", serializer.data, status.HTTP_200_OK)

    def put(self, request):
        """Updates the current user's details (e.g., currency)."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_success_response("User profile updated successfully", serializer.data, status.HTTP_200_OK)
        return api_error_response("Error updating profile", serializer.errors, status.HTTP_400_BAD_REQUEST)