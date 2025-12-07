from rest_framework import viewsets

# THis are common file that used into each apis so data will be restricted to user level
class BaseUserViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet enforcing Row-Level Security (RLS).
    Users can only see, create, update, or delete their own objects.
    """
    # The default permission (IsAuthenticated) from settings is applied here.
    
    def get_queryset(self):
        """
        Overrides queryset to filter results by the current authenticated user.
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically sets the user field during creation.
        The HiddenField in the serializer already handles this, but 
        this ensures consistency.
        """
        serializer.save(user=self.request.user)