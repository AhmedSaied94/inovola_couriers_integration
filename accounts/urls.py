from django.urls import path

from accounts.views import ConfirmSignUpView, UserSignUpView


urlpatterns = [
    path('User/', UserSignUpView.as_view()),  # post / get / put
    path('ConfirmSignUp/<str:activation_code>', ConfirmSignUpView.as_view())
]
