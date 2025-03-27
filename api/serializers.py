from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["phone"] = user.phone
        return token


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_username(self, value):
        """Ensure the username is unique"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        """Ensure the email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_phone(self, value):
        """Ensure phone number follows a valid pattern"""
        pattern = r"^\+?[0-9]{10,15}$"  # Allows optional "+" and 10-15 digits
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid phone number format.")
        return value

    def validate_password(self, value):
        """Ensure password meets security criteria"""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value

    def validate(self, data):
        """Ensure password and confirm password match"""
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")  # Remove confirm_password before saving
        user = User.objects.create_user(**validated_data)
        return user


