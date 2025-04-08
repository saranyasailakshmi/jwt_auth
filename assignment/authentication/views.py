from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserLoginSerializer, UserSignupSerializer
from .validators import UserValidator, LoginValidator


class RegisterUserAPIView(APIView):
    """
    API for registering users (email & password-based).
    Only authenticated users can register others.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        context = {"success": 1, "message": "User registered successfully", "data": {}}

        try:
            validator = UserValidator(data=request.data)
            if not validator.is_valid():
                raise serializers.ValidationError(validator.errors)

            validated_data = validator.validated_data

            # Create user
            user = CustomUser.objects.create_user(
                email=validated_data["email"],
                password=validated_data["password"],
                is_active=validated_data.get("is_active", True),
                is_staff=validated_data.get("is_staff", False)
            )

            context["data"] = UserSignupSerializer(user).data

        except serializers.ValidationError as e:
            context["success"] = 0
            context["message"] = e.detail if hasattr(e, 'detail') else str(e)
        except Exception as e:
            context["success"] = 0
            context["message"] = str(e)

        return Response(context)


class LoginAPIView(APIView):
    """
    API for logging in users using email and password.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        context = {"success": 1, "message": "Login successful", "data": {}}

        try:
            validator = LoginValidator(data=request.data)
            if not validator.is_valid():
                raise serializers.ValidationError(validator.errors)

            validated_data = validator.validated_data
            email = validated_data["email"]
            password = validated_data["password"]

            user = authenticate(request, email=email, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("Your account is inactive. Please contact admin.")

            refresh = RefreshToken.for_user(user)

            context["data"] = {
                "user": UserLoginSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }

        except serializers.ValidationError as e:
            context["success"] = 0
            context["message"] = e.detail if hasattr(e, 'detail') else str(e)
        except Exception as e:
            context["success"] = 0
            context["message"] = str(e)

        return Response(context)
