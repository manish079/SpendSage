
from .models import Transaction, Category, Budget, BackgroundTask
from .serializers import (
    CategorySerializer, 
    TransactionSerializer, 
    BudgetSerializer, 
    BackgroundTaskSerializer
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from common.utils import api_success_response, api_error_response
class CategoryAPIView(APIView):
    """
    Single endpoint for Category operations (list, create, update, delete).
    Token protected and user-specific.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Retrieve all categories or a single category for the logged-in user."""
        if pk:
            category = Category.objects.filter(user=request.user, pk=pk).first()
            if category:
                serializer = CategorySerializer(category)
                
                return api_success_response(
                message="Categories retrieved successfully",
                data=serializer.data
            )
                
            return api_error_response(
                    message="Category not found",
                        status_code=status.HTTP_404_NOT_FOUND
                    )
        
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        return api_success_response(
            message="Categories retrieved successfully",
            data=serializer.data
        )

    def post(self, request):
        """Create a new category for the logged-in user."""
        serializer = CategorySerializer(data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return api_success_response(
                message="Category created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return api_error_response(
            message="Failed to create category",
            error_details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, pk):
        """Update a specific category for the logged-in user."""
        category = Category.objects.filter(user=request.user, id=pk).first() 
        if not category:
            return api_error_response(
                message="Category not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return api_success_response(
                message="Category updated successfully",
                data=serializer.data
            )
        return api_error_response(
            message="Failed to update category",
            error_details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """Delete a specific category for the logged-in user."""
        category = Category.objects.filter(user=request.user, id=pk).first() 
        if not category:
            return api_error_response(
                message="Category not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return api_success_response(
            message="Category deleted successfully"
        )

class TransactionAPIView(APIView):
    """
    Single endpoint for Transaction operations (list, create, update, delete).
    Token protected and user-specific.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Retrieve all transactions for the logged-in user."""
        
        if pk:
            transaction = Transaction.objects.filter(user=request.user, pk=pk).first()
            if transaction:
                serializer = TransactionSerializer(transaction)
                
                return api_success_response(
                message="Transaction retrieved successfully",
                data=serializer.data
            )
                
            return api_error_response(
                    message="Transaction not found",
                        status_code=status.HTTP_404_NOT_FOUND
                    )
        
        transactions = Transaction.objects.filter(user=request.user)    
        serializer = TransactionSerializer(transactions, many=True)
        return api_success_response(
            message="Transactions retrieved successfully",
            data=serializer.data
        )

    def post(self, request):
        """Create a new transaction for the logged-in user."""
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return api_success_response(
                message="Transaction created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return api_error_response(
            message="Failed to create transaction",
            error_details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, pk):
        """Update a specific transaction for the logged-in user."""
        transaction = Transaction.objects.filter(user=request.user, id=pk).first() 
        if not transaction:
            return api_error_response(
                message="Transaction not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_success_response(
                message="Transaction updated successfully",
                data=serializer.data
            )
        return api_error_response(
            message="Failed to update transaction",
            error_details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """Delete a specific transaction for the logged-in user."""
        transaction = Transaction.objects.filter(user=request.user, id=pk).first() 
        if not transaction:
            return api_error_response(
                message="Transaction not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        transaction.delete()
        return api_success_response(
            message="Transaction deleted successfully"
        )
        
class BudgetAPIView(APIView):
    """
    Single endpoint for Budget operations (list, create, update, delete).
    Token protected and user-specific.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all budgets for the logged-in user."""
        budgets = Budget.objects.filter(user=request.user) 
        serializer = BudgetSerializer(budgets, many=True)
        return api_success_response(
            message="Budgets retrieved successfully",
            data=serializer.data
        )

    def post(self, request):
        """Create a new budget for the logged-in user."""
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return api_success_response(
                message="Budget created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return api_error_response(
            message="Failed to create budget",
            error_details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, pk):
        """Update a specific budget for the logged-in user."""
        budget = Budget.objects.filter(user=request.user, id=pk).first() 
        if not budget:
            return api_error_response(
                message="Budget not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_success_response(
                message="Budget updated successfully",
                data=serializer.data
            )
        return api_error_response(
            message="Failed to update budget",
            error_details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """Delete a specific budget for the logged-in user."""
        budget = Budget.objects.filter(user=request.user, id=pk).first() 
        if not budget:
            return api_error_response(
                message="Budget not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        budget.delete()
        return api_success_response(
            message="Budget deleted successfully"
        )

class BackgroundTaskAPIView(APIView):
    """
    Read-only endpoint for Background Tasks.
    Users can view their own asynchronous task status.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all background tasks for the logged-in user."""
        tasks = BackgroundTask.objects.filter(user=request.user) 
        serializer = BackgroundTaskSerializer(tasks, many=True)
        return api_success_response(
            message="Background tasks retrieved successfully",
            data=serializer.data
        )

    def retrieve(self, request, pk):
        """Retrieve a specific background task by ID for the logged-in user."""
        task = BackgroundTask.objects.filter(user=request.user, id=pk).first()
        if not task:
            return api_error_response(
                message="Background task not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = BackgroundTaskSerializer(task)
        return api_success_response(
            message="Background task retrieved successfully",
            data=serializer.data
        )


############ API using ModelViewSet #######################
# --- 1. Category CRUD ---
# class CategoryViewSet(BaseUserViewSet):
#     """Handles CRUD operations for user Categories."""
#     permission_classes = [IsAuthenticated]
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# # --- 2. Transaction CRUD ---
# class TransactionViewSet(BaseUserViewSet):
#     """Handles CRUD operations for user Transactions."""
#     # Optimization: Use select_related to pre-fetch the Category data (reduces DB queries)
#     permission_classes = [IsAuthenticated]
#     queryset = Transaction.objects.select_related('category').all()
#     serializer_class = TransactionSerializer

# # --- 3. Budget CRUD ---
# class BudgetViewSet(BaseUserViewSet):
#     """Handles CRUD operations for user Budgets."""
#     permission_classes = [IsAuthenticated]
#     queryset = Budget.objects.all()
#     serializer_class = BudgetSerializer

# # --- 4. Background Task Read-Only (for polling) ---
# class BackgroundTaskViewSet(BaseUserViewSet):
#     """Allows users to view the status of their asynchronous tasks."""
#     permission_classes = [IsAuthenticated]
#     queryset = BackgroundTask.objects.all()
#     serializer_class = BackgroundTaskSerializer
#     # Users can only read status, not create/delete/update the task records directly
#     http_method_names = ['get']