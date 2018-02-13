from django.test import TestCase
from ..forms import SettingsForm


class SettingsFormTest(TestCase):
    def test_form_has_fields(self):
        form = SettingsForm()
        expected = ['topics_per_page', 'location', 'birth_date',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

