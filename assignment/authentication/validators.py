from rest_framework import serializers

class UserValidator(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Email is a required field.",
            "invalid": "Enter a valid email address."
        }
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        error_messages={
            "required": "Password is a required field.",
            "min_length": "Password must be at least 8 characters long."
        }
    )
    is_active = serializers.BooleanField(
        required=False,
        default=True
    )
    is_staff = serializers.BooleanField(
        required=False,
        default=False
    )

class LoginValidator(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Email is a required field.",
            "invalid": "Enter a valid email address."
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            "required": "Password is a required field."
        }
    )