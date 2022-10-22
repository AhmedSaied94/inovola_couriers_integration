from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from accounts.serializer import UserSerializer, UserUpdateSerializer

User = get_user_model()
# Create your views here.


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


class UserSignUpView(RetrieveAPIView, CreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = []

    @method_permission_classes((IsAuthenticated,))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ConfirmSignUpView(APIView):
    model = User
    serializer_class = UserUpdateSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data={'activation_code': kwargs.get('activation_code', None)})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('success', status=status.HTTP_202_ACCEPTED)