from django.db import models
from django.contrib.auth import get_user_model
from common.models import BaseModel


User = get_user_model()


TRANSACTION_TYPE = (
    ('income', 'Income'),
    ('expense', 'Expense'),
)

TASK_STATUS = (
    ('PENDING', 'Pending'),
    ('SUCCESS', 'Success'),
    ('FAILED', 'Failed'),
)

class Category(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # NLP Seeding for Auto-Categorization (FR-07, Personal Spending Memory)
    keywords = models.TextField(
        blank=True,
        help_text="Comma-separated keywords for ML model (e.g., 'STARBUCKS, COFFEE')"
    )

    class Meta:
        unique_together = ('user', 'name')

# Expenses

class Transaction(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, help_text="The final, user-confirmed category.") # ML and Classification Fields (Modifications)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE, default='EXPENSE')
    is_anomaly = models.BooleanField(
        default=False, 
        help_text="Flagged by the ML Anomaly Detector (FR-08)."
    )
    raw_description = models.TextField(max_length=255)
    
    class Meta:
        ordering = ['-created_at', '-id']
        indexes = [models.Index(fields=['user', 'created_at'])]


class Budget(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    period_start_date = models.DateField()
    period_end_date = models.DateField()
    limit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # ML Prediction Field (Modification)
    ml_prediction_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Predicted spending by the ML model for this period."
    )
    status = models.CharField(max_length=20, default='ON_TRACK')
    
    class Meta:
        ordering = ['user', 'category', 'period_start_date']


class BackgroundTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Celery ID for tracking
    task_id = models.CharField(max_length=255, unique=True)
    task_type = models.CharField(max_length=50) 
    
    status = models.CharField(max_length=10, choices=TASK_STATUS, default='PENDING')
    result_file = models.FileField(upload_to='task_results/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)