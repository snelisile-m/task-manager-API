from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc),
                'status_code': response.status_code
            }
        }

    return response
