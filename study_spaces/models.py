"""
 REFERENCES

 Title: Python String format() Method
 Author: W3 Schools
 Date: N/A
 Code version: N/A
 URL: https://www.w3schools.com/python/ref_string_format.asp
 Software License: N/A

 Title: Model field reference
 Author: Django Project
 Date: N/A
 Code version: N/A
 URL: https://docs.djangoproject.com/en/4.2/ref/models/fields/
 Software License: N/A
 """

from django.db import models
from django.utils import timezone


class StudySpace(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    # Amenities
    has_wifi = models.BooleanField(default=False)
    has_outlets = models.BooleanField(default=False)
    has_printers = models.BooleanField(default=False)
    has_whiteboards = models.BooleanField(default=False)
    is_quiet = models.BooleanField(default=False)
    is_outside = models.BooleanField(default=False)
    has_food = models.BooleanField(default=False)

    class ApprovalStatus(models.IntegerChoices):
        APPROVED = 1
        PENDING = 0
        DENIED = -1

    approved_submission = models.IntegerField(choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    user_email = models.CharField(max_length=200)
    denial_reason = models.CharField(max_length=200, default='')
    location = models.TextField(default='')
    environment = models.TextField(default='')
    traffic = models.TextField(default='')
    hours = models.TextField(default='')
    other_information = models.TextField(default='')
    time_created = models.DateTimeField(default=timezone.now)

    def get_sentence(self):
        return "{name} is located at {address}.".format(name=self.name, address=self.address)

    def __str__(self):
        return self.name