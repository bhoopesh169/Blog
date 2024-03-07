from.models import blog_category
from django.forms import ModelForm
from.models import Comment


class Blog_Form(ModelForm):
    class Meta:
         model = blog_category
         fields = "__all__"

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']