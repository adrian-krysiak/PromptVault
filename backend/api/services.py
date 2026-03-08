from .models import Prompt

# SERVICE LAYER


def create_prompt(validated_data: dict) -> Prompt:
    """
    Create a new prompt.

    This is the place to add future business logic such as JWT author
    assignment, creation limits, or external storage integrations.
    """
    # Save to DB using the repository (model manager)
    return Prompt.objects.create(**validated_data)


def deactivate_prompt(prompt: Prompt) -> Prompt:
    """
    Perform a soft delete by marking the prompt as inactive.
    """
    prompt.is_active = False
    prompt.save()
    return prompt
