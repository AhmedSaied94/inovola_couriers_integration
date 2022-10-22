from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        return User.objects.create_user(email, password, **validated_data)


class UserUpdateSerializer(serializers.Serializer):
    activation_code = serializers.CharField()

    class Meta:
        fields = ('activation_code',)

    def validate(self, attrs):
        try:
            if not self.context['request'].user.is_authenticated:
                user = User.objects.get(
                    activation_code=attrs['activation_code'])
        except:
            raise serializers.ValidationError(
                "Invalid or expired link", code=400)

        return {**attrs, "activation_code": user}

    def save(self, **kwargs):
        user = kwargs.pop('user')
        user.is_active = True
        user.save()

        return user
