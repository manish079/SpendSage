from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email


class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(style={'input_type' : 'password'}, write_only = True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'phone_number', 'is_active', 'is_staff', 'is_superuser']
        
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
            username=validate_data['username'],
            password=validate_data['password'],
            currency_preference=validate_data.get('currency_preference', 'INR')
        )
        
        return user
        
        
         