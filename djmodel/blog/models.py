from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone

# Create your models here.

from .validators import validate_author_email, validate_admin

PUBLISH_CHOICES = (
		("draft", "Draft"),
		("publish", "Publish"),
		("private", "Private"),
	)

class PostModel(models.Model):
	active        = models.BooleanField(default=True)
	nonactive     = models.NullBooleanField(default=True)
	title         = models.CharField(max_length=30, verbose_name="Title", unique=True)
	description   = models.TextField(null=True, blank=True)
	publish       = models.CharField(max_length=120, choices=PUBLISH_CHOICES , default="draft")
	view_count    = models.IntegerField(default=0)
	publish_date  = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
	author_email  = models.CharField(max_length=240, validators=[validate_author_email, validate_admin], null=True, blank=True)
	second_author = models.EmailField(max_length=240, null=True, blank=True)

	class Meta:
		verbose_name = "Post"
		verbose_name_plural = "Posts"
		# unique_together = [("title", "description")]

	# def __str__(self):
	# 	return self.title

	
	def __str__(self):
		return smart_text(self.title)