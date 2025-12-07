from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Modified default rest framework to return id and email into login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # this gives 'access' and 'refresh'
        
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        return data
    
class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(style={'input_type' : 'password'}, write_only = True, required = True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        
    def validate_email(self, value):
        """Validate email format and uniqueness."""
        try:
            validate_email(value)
        except:
            raise serializers.ValidationError("Enter a valid email address.")
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validate_data):
        user = User.objects.create_user(  # create_user store password into hash formate
            email=validate_data['email'],
            first_name=validate_data['first_name'],
            last_name=validate_data['last_name'],
            username=validate_data['email'],
            password=validate_data['password'],
            currency_preference=validate_data.get('currency_preference', 'INR')
        )
        
        return user
        
        
         