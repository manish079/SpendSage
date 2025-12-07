import pytz
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response

def api_success_response(message, data=None, status_code=status.HTTP_200_OK):
    """Standardized success response."""
    response = {
        "status": True,
        "message": message,
        "data": data if data else {}
    }
    return Response(response, status=status_code)

def api_error_response(message, error_details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """Standardized error response."""
    response = {
        "status": False,
        "message": message,
        "error": error_details if error_details else {}
    }
    return Response(response, status=status_code)
