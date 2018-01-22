from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.encoding import smart_text
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

from .validators import validate_author_email, validate_admin

PUBLISH_CHOICES = (
		("draft", "Draft"),
		("publish", "Publish"),
		("private", "Private"),
	)


class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,
					 self).get_queryset()\
						  .filter(status="published")


class PostModel(models.Model):
	active        = models.BooleanField(default=True)
	nonactive     = models.NullBooleanField(default=True)
	title         = models.CharField(
							max_length=30, 
							verbose_name="Title", 
							unique=True,
							error_messages={
								"unique": "This title is not unique. Please try again",
								"blank": "This field has to be filled"
								},
							help_text="This field is important for the user",
							)
	description   = models.TextField(null=True, blank=True)
	slug          = models.SlugField(max_length=250, null=True, blank=True, editable=False)
	publish       = models.CharField(max_length=120, choices=PUBLISH_CHOICES , default="draft")
	view_count    = models.IntegerField(default=0)
	publish_date  = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
	author_email  = models.CharField(max_length=240, validators=[validate_author_email, validate_admin], null=True, blank=True)
	second_author = models.EmailField(max_length=240, null=True, blank=True)
	updated		  = models.DateTimeField(auto_now=True)
	timestamp     = models.DateTimeField(auto_now_add=True)
	objects       = models.Manager()
	published     = PublishedManager()

	def save(self, *args, **kwargs):
		if not self.slug:
			if self.title:
				self.slug = slugify(self.title)
		# print("Hello there")
		# self.title = "A new title" #overriding post title
		super(PostModel, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Post"
		verbose_name_plural = "Posts"
		# unique_together = [("title", "description")]

	# def __str__(self):
	# 	return self.title

	
	def __str__(self):
		return smart_text(self.title)


# def blog_post_model_pre_save_receiver():
# 	pass

# def blog_post_model_post_save_receiver(semder. instance, created, *args, **kwargs):
# 	if not instance.slug and instance.title:
# 		instance.slug = slugify(instance.title)
# 		instance.save()

# pre_save.connect(blog_post_model_pre_save_receiver, sender=PostModel)

# post_save_connect(blog_post_model_pre_save_receiver, sender=PostModel)