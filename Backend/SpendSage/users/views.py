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
            
            return Response(api_success_response(user), status = status.HTTP_201_CREATED)
        
        return Response(api_error_response(serializer.errors), status = status.HTTP_400_BAD_REQUEST)   

class UserProfileView(APIView):
    """
    Protected endpoint to view and update the logged-in user's profile.
    Requires a valid JWT token.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retrieves the current user's details."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """Updates the current user's details (e.g., currency)."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)  