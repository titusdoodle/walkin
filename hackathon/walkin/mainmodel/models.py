from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
	name = models.CharField(max_length=30)
	company_type = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Freelancer(models.Model):
	user_id = models.ForeignKey(User)
	company = models.ForeignKey(Company)
	skill = models.CharField(max_length=500)

	def __str__(self):
		return str(self.user_id)

class userlikes(models.Model):
	user_id = models.ForeignKey(User)
	company_likes = models.CharField(max_length=500, blank=True)
	skill_likes = models.CharField(max_length=500, blank=True)

	def __str__(self):
		return str(self.user_id)

class Project(models.Model):
	user_id = models.ForeignKey(User)
	name = models.CharField(max_length=500, blank=True)
	email = models.CharField(max_length=500, blank=True)
	proj_type = models.CharField(max_length=500, blank=True)
	description = models.CharField(max_length=500, blank=True)
	budget = models.CharField(max_length=500, blank=True)

	def __str__(self):
		return str(self.user_id)