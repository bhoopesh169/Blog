from django.contrib import admin
from.models import blog_category, contact_info, Subscription
from.models import Blog_post, Comment
# Register your models here.

admin.site.register(blog_category)
admin.site.register(contact_info)
admin.site.register(Subscription)
admin.site.register(Blog_post)
admin.site.register(Comment)