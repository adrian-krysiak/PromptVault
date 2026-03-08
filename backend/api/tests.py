from rest_framework import status
from rest_framework.test import APITestCase

from .models import Prompt


class PromptApiTests(APITestCase):
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
