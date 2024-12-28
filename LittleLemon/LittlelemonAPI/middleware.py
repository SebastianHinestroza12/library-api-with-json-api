import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler

class JSONAPIExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        response = drf_exception_handler(exception, context=None)
        if response is not None:
            response.data = {
                "errors": [
                    {
                        "detail": response.data.get('detail', 'An error occurred'),
                        "status": str(response.status_code),
                        "code": response.data.get('code', 'error')
                    }
                ]
            }
            return JsonResponse(response.data, status=response.status_code)
        return JsonResponse({
            "errors": [
                {
                    "detail": str(exception),
                    "status": str(status.HTTP_500_INTERNAL_SERVER_ERROR),
                    "code": "internal_server_error"
                }
            ]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
