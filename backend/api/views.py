from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Prompt
from .serializers import PromptSerializer
from . import services


# CONTROLLER LAYER
class PromptViewSet(viewsets.ModelViewSet):
    """
    Equivalent of a .NET controller.
    It handles HTTP routing and delegates business logic to the service layer.
    Provides CRUD endpoints: list, retrieve, create, update, and delete.
    """

    # Read data through our repository layer (custom manager).
    queryset = Prompt.objects.active()
    serializer_class = PromptSerializer

    def perform_create(self, serializer):
        # DRF validates request data before this hook is called.
        # Set serializer.instance so the response includes created object fields.
        serializer.instance = services.create_prompt(
            validated_data=serializer.validated_data
        )

    def destroy(self, request, *args, **kwargs):
        # Override delete to use business-layer soft delete.
        prompt = self.get_object()
        services.deactivate_prompt(prompt)
        return Response(status=status.HTTP_204_NO_CONTENT)
