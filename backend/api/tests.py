from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Prompt
from .serializers import PromptReadSerializer, PromptWriteSerializer
from .services import create_prompt, deactivate_prompt


class PromptApiTests(APITestCase):
    def _create_prompt(self, title="Test prompt", content="Sample content"):
        return Prompt.objects.create(title=title, content=content)

    def test_create_list_and_soft_delete_prompt(self):
        list_url = "/api/prompts/"

        create_response = self.client.post(
            list_url,
            data={"title": "Test prompt", "content": "Sample content"},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        prompt_id = create_response.data["id"]

        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["id"], prompt_id)

        delete_response = self.client.delete(f"/api/prompts/{prompt_id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        prompt = Prompt.objects.get(pk=prompt_id)
        self.assertFalse(prompt.is_active)

        list_after_delete_response = self.client.get(list_url)
        self.assertEqual(list_after_delete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_after_delete_response.data), 0)

    def test_retrieve_prompt_returns_200(self):
        prompt = self._create_prompt()

        response = self.client.get(f"/api/prompts/{prompt.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], prompt.id)

    def test_update_prompt_returns_200(self):
        prompt = self._create_prompt()

        response = self.client.patch(
            f"/api/prompts/{prompt.id}/",
            data={"title": "Updated title"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated title")

    def test_full_update_prompt_with_put_returns_200(self):
        prompt = self._create_prompt(title="Old", content="Old content")

        response = self.client.put(
            f"/api/prompts/{prompt.id}/",
            data={"title": "New", "content": "New content", "is_active": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New")
        self.assertEqual(response.data["content"], "New content")

    def test_full_update_with_invalid_payload_returns_400(self):
        prompt = self._create_prompt()

        response = self.client.put(
            f"/api/prompts/{prompt.id}/",
            data={"title": "Missing content"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_returns_only_active_prompts(self):
        active_prompt = self._create_prompt(title="Visible")
        hidden_prompt = self._create_prompt(title="Hidden")
        hidden_prompt.is_active = False
        hidden_prompt.save()

        response = self.client.get("/api/prompts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], active_prompt.id)

    def test_create_with_invalid_payload_returns_400(self):
        response = self.client.post(
            "/api/prompts/",
            data={"content": "Missing title"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_prompt_returns_404(self):
        response = self.client.get("/api/prompts/999999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_prompt_returns_404(self):
        response = self.client.delete("/api/prompts/999999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_soft_deleted_prompt_returns_404_on_retrieve(self):
        prompt = self._create_prompt()
        self.client.delete(f"/api/prompts/{prompt.id}/")

        response = self.client.get(f"/api/prompts/{prompt.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed_returns_405(self):
        prompt = self._create_prompt()

        response = self.client.post(
            f"/api/prompts/{prompt.id}/",
            data={"title": "Not allowed on detail"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PromptServiceTests(TestCase):
    def test_create_prompt_creates_active_prompt(self):
        prompt = create_prompt({"title": "Service title", "content": "Service content"})

        self.assertTrue(Prompt.objects.filter(pk=prompt.pk).exists())
        self.assertTrue(prompt.is_active)

    def test_deactivate_prompt_sets_inactive_flag(self):
        prompt = Prompt.objects.create(title="To delete", content="Content")

        deactivated = deactivate_prompt(prompt)

        self.assertFalse(deactivated.is_active)
        prompt.refresh_from_db()
        self.assertFalse(prompt.is_active)


class PromptModelAndSerializerTests(TestCase):
    def test_prompt_str_returns_title(self):
        prompt = Prompt.objects.create(title="Readable title", content="Body")

        self.assertEqual(str(prompt), "Readable title")

    def test_active_queryset_returns_only_active_records(self):
        active_prompt = Prompt.objects.create(title="Active", content="A")
        Prompt.objects.create(title="Inactive", content="B", is_active=False)

        active_records = Prompt.objects.active()

        self.assertEqual(active_records.count(), 1)
        self.assertEqual(active_records.first().id, active_prompt.id)

    def test_write_serializer_ignores_read_only_fields(self):
        """Test that PromptWriteSerializer only accepts title and content."""
        serializer = PromptWriteSerializer(
            data={
                "id": 999,
                "title": "Serializer title",
                "content": "Serializer content",
                "is_active": True,
                "created_at": "2020-01-01T00:00:00Z",
                "updated_at": "2020-01-01T00:00:00Z",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        prompt = serializer.save()

        # Verify that the extraneous fields were ignored
        self.assertNotEqual(prompt.id, 999)
        self.assertTrue(prompt.is_active)  # Default value

    def test_read_serializer_includes_all_fields(self):
        """Test that PromptReadSerializer includes id and timestamps as read-only."""
        prompt = Prompt.objects.create(title="Test", content="Content")
        serializer = PromptReadSerializer(prompt)

        self.assertIn("id", serializer.data)
        self.assertIn("created_at", serializer.data)
        self.assertIn("updated_at", serializer.data)
        self.assertEqual(serializer.data["title"], "Test")
        self.assertEqual(serializer.data["content"], "Content")
