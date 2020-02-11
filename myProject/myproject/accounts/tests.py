from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from .views import signup
from django.contrib.auth.models import User
from .form import SignUpForm


class SignUpTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_sign_up_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)


class SuccessfulSignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        """
        a valid form submission should redirect the user to the home page
        :return:
        """
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """
        Create a new request to an arbitrary page
        The resulting response should now have a 'user' to its context,
        after a successful sign up
        :return:
        """
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignupTests(TestCase):
    def setUp(self) -> None:
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        """
        an invalid form submission should return to the same page
        :return:
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_error(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
