from django.urls import path
from .views import CategoryAPIView, TransactionAPIView, BudgetAPIView, BackgroundTaskAPIView

urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryAPIView.as_view()),
    path('expenses_trans/', TransactionAPIView.as_view(), name='expenses_trans'),
    path('expenses_trans/<int:pk>/', TransactionAPIView.as_view(), name='expenses_trans'),
    path('expenses/', TransactionAPIView.as_view(), name='expenses'),
    path('budgets/', BudgetAPIView.as_view(), name='budgets'),
    path('tasks/', BackgroundTaskAPIView.as_view(), name='tasks'),
]
