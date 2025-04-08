from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .models import Product
from .serializers import ProductSerializer
from .validators import ProductValidator


# 1. Create Product View
class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        context = {"success": 1, "message": "Product created successfully", "data": {}}
        try:
            validator = ProductValidator(data=request.data)
            if not validator.is_valid():
                raise serializers.ValidationError(validator.errors)

            validated_data = validator.validated_data
            product = Product.objects.create(**validated_data)
            context["data"] = ProductSerializer(product).data

        except serializers.ValidationError as e:
            context["success"] = 0
            context["message"] = e.detail if hasattr(e, "detail") else str(e)
        except Exception as e:
            context["success"] = 0
            context["message"] = str(e)

        return Response(context)


# 2. Get All Products
class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {"success": 1, "message": "Product list retrieved", "data": {}}
        try:
            products = Product.objects.all()
            context["data"] = ProductSerializer(products, many=True).data
        except Exception as e:
            context["success"] = 0
            context["message"] = str(e)

        return Response(context)


# 3. Update Product
class ProductUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def put(self, request, pk):
        context = {"success": 1, "message": "Product updated successfully", "data": {}}
        try:
            product = self.get_object(pk)
            if not product:
                raise serializers.ValidationError("Product not found.")

            validator = ProductValidator(data=request.data)
            if not validator.is_valid():
                raise serializers.ValidationError(validator.errors)

            validated_data = validator.validated_data

            for attr, value in validated_data.items():
                setattr(product, attr, value)
            product.save()

            context["data"] = ProductSerializer(product).data

        except serializers.ValidationError as e:
            context["success"] = 0
            context["message"] = e.detail
        except Exception as e:
            context["success"] = 0
            context["message"] = str(e)

        return Response(context)


# 4. Delete Product
class ProductDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def delete(self, request, pk):
        context = {"success": 1, "message": "Product deleted successfully", "data": {}}
        try:
            product = self.get_object(pk)
            if not product:
                raise serializers.ValidationError("Product not found.")

            product.delete()

        except serializers.ValidationError as e:
            context["success"] = 0
            context["message"] = e.detail
        except Exception as e:
            context["success"] = 0
            context["message"] = str(e)

        return Response(context)
