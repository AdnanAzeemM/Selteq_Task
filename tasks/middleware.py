from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .models import CustomUser, Task


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ['/api/post_tasks/', '/api/get_tasks']:
            # check authentication
            auth_header = request.headers.get('Authorization')

            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse(
                    {'detail': 'Authentication credentials were not provided.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            try:
                token = auth_header.split(' ')[1]
                access_token = AccessToken(token)

                user = CustomUser.objects.get(id=access_token['user_id'])
                request.user = user

            except Exception as e:
                return JsonResponse(
                    {'detail': 'Invalid or expired token.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # check authorization
            if not self.has_permission(request):
                return JsonResponse({"error": "Unauthorized. Insufficient permissions."},
                                    status=status.HTTP_403_FORBIDDEN)

        response = self.get_response(request)
        return response

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.is_premium

