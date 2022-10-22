from django.urls import path

from accounts.views import ConfirmSignUpView, UserSignUpView


urlpatterns = [
    path('Signup/', UserSignUpView.as_view()),
    path('ConfirmSignUp/', ConfirmSignUpView.as_view())
]
