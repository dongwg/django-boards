from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from ..views import update_profile
from ..forms import SettingsForm
from ..models import Profile

class UpdateProfileTestCase(TestCase):
    '''
    Base test case to be used in all `update_profile` view tests
    '''
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username,
                email='john@doe.com', password=self.password)
        user.save()

        #self.profile = Profile.objects.create(user=user)
        self.url = reverse('boards_settings')


class LoginRequiredUpdateProfileTests(UpdateProfileTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response,
                '{login_url}?next={url}'.format(login_url=login_url,
                    url=self.url))


class UpdateProfileTests(UpdateProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_update_profile_status_code(self):
        self.assertEquals(self.response.status_code, 200)


    def test_update_profile_url_resolves_update_profile_view(self):
        view = resolve('/settings/boards/')
        self.assertEquals(view.func, update_profile)


    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SettingsForm)


    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email, password1,
        password2
        '''
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="number"', 1)
        self.assertContains(self.response, 'type="text"', 2)


class SuccessfulUpdateProfileTests(UpdateProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        data = {
                'topics_per_page': '10',
                'location': 'dummy',
                'birth_date': '1970-01-01',
                }
        self.response = self.client.post(self.url, data)
        self.home_url = reverse('home')

    def test_profile_updating(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` with updated profile to its context,
        after a successful submission.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertEquals(user.profile.topics_per_page, 10)



class InvalidUpdateProfileTests(UpdateProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})   # submit an empty

    def test_update_profile_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)


    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

