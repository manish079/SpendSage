
from rest_framework import serializers
from .models import Category, Transaction, Budget, BackgroundTask
from django.db import transaction
from rest_framework.views import exception_handler

class CurrentUserDefault:
    """Sets the user field automatically to the logged-in user."""
    requires_context = True
    def __call__(self, serializer_field):
        return serializer_field.context['request'].user

class CategorySerializer(serializers.ModelSerializer):
    """Handles Category CRUD."""
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'keywords']
        read_only_fields = ['user']

class TransactionSerializer(serializers.ModelSerializer):
    """Handles Transaction CRUD and integrates ML/Anomaly fields."""
    user = serializers.HiddenField(default=CurrentUserDefault())
    
    category_name = serializers.CharField(source='category.name', read_only=True) 

    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'amount', 'raw_description', 
            'category', 'category_name', 'is_anomaly', 'transaction_type'
        ]
        # is_anomaly is set by the service layer/ML model, not the user
        read_only_fields = ['is_anomaly'] 
        
    @transaction.atomic 
    def create(self, validated_data):
        # NOTE: The actual ML/Anomaly logic will be handled 
        # in the TransactionService layer
        return Transaction.objects.create(**validated_data)

class BudgetSerializer(serializers.ModelSerializer):
    """Handles Budget CRUD and exposes ML prediction field."""
    user = serializers.HiddenField(default=CurrentUserDefault())
    
    class Meta:
        model = Budget
        fields = [
            'id', 'user', 'category', 'period_start_date', 'period_end_date', 
            'limit_amount', 'ml_prediction_amount', 'status'
        ]
        # Prediction amount is set by the Time Series Model, not the user
        read_only_fields = ['ml_prediction_amount', 'status']

class BackgroundTaskSerializer(serializers.ModelSerializer):
    """Handles tracking status of async jobs (FR-13, FR-14)."""
    user = serializers.HiddenField(default=CurrentUserDefault())
    
    class Meta:
        model = BackgroundTask
        fields = [
            'id', 'user', 'task_id', 'task_type', 'status', 'created_at', 'result_file'
        ]
        # All fields are read-only except for the initial creation/viewing
        read_only_fields = ['task_id', 'status', 'created_at', 'result_file']