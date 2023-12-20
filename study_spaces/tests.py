"""
 REFERENCES

 Title: Introducing automated testing
 Author: Django Project
 Date: N/A
 Code version: N/A
 URL: https://docs.djangoproject.com/en/4.2/intro/tutorial05/
 Software License: N/A
 
 Title: N/A
 Author: ChatGPT
 Date: N/A
 Code version: N/A
 URL: https://chat.openai.com/
 Software License: N/A
 """

from django.test import TestCase
from study_spaces.models import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from allauth.socialaccount.models import SocialApp, SocialAccount
from django.conf import settings
import os


# Create your tests here.

class StudySpaceModelTestCase(TestCase):
    def setUp(self):
        StudySpace.objects.create(name="Rice Hall", address="85 Engineer's Way, Charlottesville, VA 22903",
                                  latitude=38.03163727267092, longitude=-78.51082838815206)
        StudySpace.objects.create(name="Thornton Stacks A-Wing", address="351 McCormick Rd, Charlottesville, VA 22904",
                                  latitude=38.03332547566759, longitude=-78.50945079424223)

    def test_model_string(self):
        rice_hall = StudySpace.objects.get(name="Rice Hall")
        thornton = StudySpace.objects.get(name="Thornton Stacks A-Wing")
        rice_sentence = rice_hall.get_sentence()
        thornton_sentence = thornton.get_sentence()
        self.assertEqual(rice_sentence, "Rice Hall is located at 85 Engineer's Way, Charlottesville, VA 22903.")
        self.assertEqual(thornton_sentence,
                         "Thornton Stacks A-Wing is located at 351 McCormick Rd, Charlottesville, VA 22904.")


class LoggedOutTests(TestCase):
    def test_redirect(self):

        response = self.client.get(reverse("study_spaces:directions"))
        response2 = self.client.get(reverse("study_spaces:profile"))
        response3 = self.client.get(reverse("study_spaces:submission"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

class NavigationBarTests(TestCase):

    # Note: used ChatGPT for how to set up the google app login for unit tests. Citation is at the top of the document

    def setUp(self):
        self.user = User.objects.create_user(username='studyspace', password='studyspacepassword')
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id = getattr(settings, 'CLIENT_ID', 'default_client_id'),
            secret = getattr(settings, 'CLIENT_SECRET', 'default_client_secret')
        )
        SocialAccount.objects.create(
            user=self.user,
            provider=google_app.provider,
            uid='test',
        )
    def test_home_link(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.get(reverse("study_spaces:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/study/"')

    def test_directions_link(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.get(reverse("study_spaces:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/study/directions"')

    def test_profile_link(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.get(reverse("study_spaces:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/study/profile"')

    def test_submission_link(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.get(reverse("study_spaces:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/study/submission"')

    def test_closest_link(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.get(reverse("study_spaces:closest"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/study/closest"')


class FeatureTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='studyspace', password='studyspacepassword', email='test@studyspaces.com')
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id = getattr(settings, 'CLIENT_ID', 'default_client_id'),
            secret = getattr(settings, 'CLIENT_SECRET', 'default_client_secret')
        )
        SocialAccount.objects.create(
            user=self.user,
            provider=google_app.provider,
            uid='test',
        )
        newModel = StudySpace(
            name='Rice Hall',
            address="85 Engineer's Way, Charlottesville, VA 22903",
            latitude = 38.03162799401157,
            longitude = -78.51084803374002,
            approved_submission = 1,
            user_email = '',
            denial_reason = '',
            other_information = 'Location: Located on Engineering Way, home to the Computer Science Department',
        )
        newModel.save()
        newModel2 = StudySpace(
            name='Clark Hall',
            address="291 McCormick Rd, Charlottesville, VA 22903",
            latitude = 38.0330428,
            longitude = -78.5078494,
            approved_submission = 1,
            user_email = '',
            denial_reason = '',
            other_information = 'Location: Located on McCormick Road closer to Amphitheater',
        )
        newModel2.save()

    def test_login(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.get("/study/")
        self.assertEqual(response.status_code, 200)
    
    def test_profile(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.get(reverse("study_spaces:profile"))
        self.assertContains(response, 'studyspace')

    def test_google_maps_page(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.get(reverse("study_spaces:directions"))
        self.assertEqual(response.status_code, 200)

    def test_more_information(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        context = {'dest': 1}
        response = self.client.get(reverse("study_spaces:information"), data=context)
        self.assertContains(response, 'Location: Located on Engineering Way, home to the Computer Science Department')
    
    def test_get_directions(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        data = {
            'lat_a': '38.0515639',
            'long_a': '-78.5099015',
            'lat_b': '38.03162799401157',
            'long_b': '-78.51084803374002',
        }
        response = self.client.get(reverse("study_spaces:directions"), data=data)
        #print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<strong>Distance:</strong> 1.7 mi')

    def test_find_closest_study_space(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        context = {'address': '568 Buckler Rd, Charlottesville, VA  22903', 'lat': '38.051555', 'long': '-78.5098917'}
        response = self.client.post(reverse("study_spaces:closest"), data=context)

        # this is checking whether or not clark hall is coming before rice hall once the page is loaded (it should)
        self.assertContains(response, '<h5>Clark Hall</h5>\n\t\t\t<p>291 McCormick Rd, Charlottesville, VA 22903</p>\n\t\t\t<a href="/study/directions?dest=2" class="btn primary-button">Get Directions</a>\n\t\t\t<br />\n\t\t\t<br />\n\t\t\t<br />\n\t\t\t\n\t\t\t<h5>Rice Hall</h5>')
    
    def test_submit_a_study_space(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        context = {'name': 'Test Space', 'address': "85 Engineer's Way, Charlottesville, VA 22903", 'lat': '38.03162799401157', 'long': '-78.51084803374002',
                    'location': "Test Space", 'environment': 'Test', 'traffic': 'Test', 'hours': 'Test', 'other_information': 'test'}
        response = self.client.post(reverse('study_spaces:submission'), data=context)
        self.assertEqual(response.status_code, 200)
        response_2 = self.client.get(reverse('study_spaces:submission'))
        self.assertContains(response_2, 'Past Submissions</h3>\n\t\t\t\t\t \n\t\t\t\t\t<div class="mb-3 p-3 submission-section">\n\t\t\t\t\t\t<span class="d-flex">\n\t\t\t\t\t\t\t<strong>Study Space Name:</strong>\n\t\t\t\t\t\t\t<p class="mx-2">Test Space</p>')
                                    

class AdminTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='studyspace', password='studyspacepassword', email='lukecreech11@gmail.com')
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id = getattr(settings, 'CLIENT_ID', 'default_client_id'),
            secret = getattr(settings, 'CLIENT_SECRET', 'default_client_secret')
        )
        SocialAccount.objects.create(
            user=self.user,
            provider=google_app.provider,
            uid='test',
        )
        newModel = StudySpace(
            name='Rice Hall',
            address="85 Engineer's Way, Charlottesville, VA 22903",
            latitude = 38.03162799401157,
            longitude = -78.51084803374002,
            approved_submission = 0,
            user_email = 'test@studyspaces.com',
            denial_reason = '',
            other_information = 'Location: Located on Engineering Way, home to the Computer Science Department',
        )
        newModel.save()
        newModel2 = StudySpace(
            name='Clark Hall',
            address="123 Main St.",
            latitude = 38.0330428,
            longitude = -78.5078494,
            approved_submission = 0,
            user_email = 'test@studyspaces.com',
            denial_reason = '',
            other_information = 'Location: Located on McCormick Road closer to Amphitheater',
        )
        newModel2.save()
        
    def test_admin_profile(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.get(reverse("study_spaces:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>You are an admin</p>')

    def test_approve_submission(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        context = {'id': 1}
        test_model = StudySpace.objects.get(pk=1)
        response = self.client.post(reverse('study_spaces:approve'), data=context)
        self.assertEqual(response.status_code, 302)
        test_model.refresh_from_db()
        self.assertEqual(test_model.approved_submission, StudySpace.ApprovalStatus.APPROVED)

    def test_deny_submission(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        context = {'id': 2, 'Denial': 'Wrong Address Given'}
        test_model = StudySpace.objects.get(pk=2)
        response = self.client.post(reverse('study_spaces:deny'), data=context)
        self.assertEqual(response.status_code, 302)
        test_model.refresh_from_db()
        self.assertEqual(test_model.approved_submission, StudySpace.ApprovalStatus.DENIED)

    def test_edit_study_space(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        test_space = StudySpace.objects.get(pk=1)
        old_name = test_space.name
        new_name = 'New Test Name'
        context = {'name': 'New Test Name', 'address': "85 Engineer's Way, Charlottesville, VA 22903", 'lat': '38.03162799401157', 'long': '-78.51084803374002',
                   'location': "Test Space", 'environment': 'Test', 'traffic': 'Test', 'hours': 'Test', 'other_information': 'test'}
        response = self.client.post(reverse('study_spaces:edit', kwargs={'study_space_id': 1}), data=context)
        test_space.refresh_from_db()
        self.assertNotEqual(old_name, test_space.name)
        self.assertEqual(new_name, test_space.name)
        
    def test_delete_study_space(self):
        self.client.login(username='studyspace', password='studyspacepassword')
        response = self.client.post(reverse('study_spaces:delete', kwargs={'study_space_id': 1}))
        response = self.client.post(reverse('study_spaces:delete', kwargs={'study_space_id': 2}))
        self.assertEqual(0, StudySpace.objects.count())


