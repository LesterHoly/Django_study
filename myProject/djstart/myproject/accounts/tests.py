from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from .views import signup


class SignUpTest(TestCase):

    def setUp(self):
        pass

    def test_sign_up_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

