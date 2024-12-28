from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = []
        if isinstance(response.data, list):
            for error in response.data:
                errors.append({
                    "status": response.status_code,
                    "detail": error
                })
        else:
            for key, value in response.data.items():
                if isinstance(value, list):
                    for val in value:
                        errors.append({
                            "status": response.status_code,
                            "source": {"pointer": key},
                            "detail": val
                        })
                else:
                    errors.append({
                        "status": response.status_code,
                        "source": {"pointer": key},
                        "detail": value
                    })

        response.data = {
            "errors": errors
        }

    return response
