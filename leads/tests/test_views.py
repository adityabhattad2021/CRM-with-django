from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class LandingPageTest(TestCase):

    def test_get(self):
        response=self.client.get(reverse('main-page'))
        self.assertTemplateUsed(response,'main.html')