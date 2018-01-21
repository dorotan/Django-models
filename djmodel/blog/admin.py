from django.contrib import admin

# Register your models here.

from .models import PostModel

class PostAdmin(admin.ModelAdmin):

	list_display        = ("title", "slug", "publish_date", "timestamp")
	list_filter         = ("publish", "author_email")
	search_fields       = ("title", "description")
	ordering            = ["publish"]

	fields              = [
		"title",   
		"description",   
		"slug",
		"publish",       
		"publish_date",
		"author_email",
		"second_author",
		"updated",
		"timestamp",
		"new_content",   
	]

	readonly_fields     = ["slug", "updated", "timestamp", "new_content"]

	def new_content(self, obj, *args, **kwargs):
		return str(obj.title)


	class Meta:
		model = PostModel

admin.site.register(PostModel, PostAdmin)