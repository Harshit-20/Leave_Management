# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User;
from django.db.models.signals import post_save
from django.dispatch import receiver
from userprofile.models import FacultyProfile
# Create your models here. 
LEAVE_CHIOCE = (
	('casual', 'Casual Leave'),
    ('vacation', 'Vacation Leave'),
    ('commuted', 'Commuted Leave'),
    ('special_casual', 'Special Casual Leave'),
    ('restricted', 'Restricted Leave'),
    ('station', 'Station Leave'),
)

APPLICATION_STATUSES = (

    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('processing', 'Being Processed')

)


class Leave(models.Model):
	leave_id = models.IntegerField(null=True);
	# user = models.CharField(max_length=100);
	user = models.ForeignKey(User,related_name='applied_for', on_delete=models.CASCADE);
	replacing_user = models.ForeignKey(User, related_name='replaced_for', on_delete=models.CASCADE)
	leave_type = models.CharField(max_length=20, choices=LEAVE_CHIOCE);
	applied_time = models.DateTimeField(auto_now = True);
	start_date = models.DateField();
	end_date = models.DateField();
	purpose = models.CharField(max_length=500, blank=True);
	leave_address = models.CharField(max_length=100, blank=True);
	processing_status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='processing');
	leaveto = models.CharField(max_length=100)
	def __str__(self):
		return '{} - {}'.format(self.user.username, self.leave_type)

	def save(self, *args, **kwargs):
		if (self.start_date <= self.end_date):
			super(Leave, self).save(*args, **kwargs);
		else:
			raise Exception("Start Date Should be less than(or equal to) the End Date");

class ApplicationRequest(models.Model):
	user = models.ForeignKey(User, related_name='requested_applications', on_delete= models.CASCADE);
	recipient = models.ForeignKey(User, related_name="application_request", on_delete=models.CASCADE )
	leave = models.ForeignKey(Leave, related_name='pending_request', on_delete=models.CASCADE);
	def __str__(self):
		return '{}: {}'.format(self.user.username, self.leave.leave_type);


class RemainingLeaves(models.Model):
	user = models.OneToOneField(User, related_name='remaining_leave', on_delete=models.CASCADE);
	casual = models.IntegerField(default=30);
	vacation = models.IntegerField(default=60);
	commuted = models.IntegerField(default=10);
	special_casual = models.IntegerField(default=15);
	restricted = models.IntegerField(default = 2)

	def __str__(self):
		return '{} has {} casual leaves left'.format(self.user.username, self.casual)


@receiver(post_save, sender=FacultyProfile)
def create_remaining_leaves(sender, instance, created, **kwargs):
    if created:
        RemainingLeaves.objects.create(user=instance.user)
