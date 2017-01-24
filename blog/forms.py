from django import forms
from django.utils import timezone

from pagedown.widgets import PagedownWidget

from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(required=False, widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = ['title','content','image','draft','publish']

    def clean_publish(self):
        draft = self.cleaned_data.get('draft')
        publish = self.cleaned_data.get('publish')
        today = timezone.now().date()
        if not draft:
            if not publish:
                raise forms.ValidationError("only drafts can be saved without a publish date")
        if publish < today:
            raise forms.ValidationError("publish date can't be in the past")
        print (publish, today)
        return publish
