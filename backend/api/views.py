from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Prompt
from .serializers import PromptReadSerializer, PromptWriteSerializer
from . import services


# CONTROLLER LAYER
class PromptViewSet(viewsets.ModelViewSet):
    """
    Equivalent of a .NET controller.
    It handles HTTP routing and delegates business logic to the service layer.
    Provides CRUD endpoints: list, retrieve, create, update, and delete.
    """

    # Read data through repository layer (custom manager).
    queryset = Prompt.objects.active()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PromptWriteSerializer
        return PromptReadSerializer

    def create(self, request, *args, **kwargs):
        # DRF validates request data before this hook is called.
        # Set serializer.instance so the response includes created object fields.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.instance = services.create_prompt(
            validated_data=serializer.validated_data
        )
        
        read_serializer = PromptReadSerializer(serializer.instance)
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # Use PromptWriteSerializer for validation, but return PromptReadSerializer response
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        read_serializer = PromptReadSerializer(serializer.instance)
        return Response(read_serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Override delete to use business-layer soft delete.
        prompt = self.get_object()
        services.deactivate_prompt(prompt)
        return Response(status=status.HTTP_204_NO_CONTENT)
