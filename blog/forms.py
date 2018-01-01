from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from pagedown.widgets import PagedownWidget

from .models import Post, Location, LocationImage, Image

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'suburb', 'phone_number','cuisine', 'loc_type', 'maplink', 'website', 'delivery_avaiable', 'rating']


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Image
        fields = ['image']

    def clean(self):
        cleaned_data = super(ImageForm, self).clean()
        location = cleaned_data.get('location')
        climage = cleaned_data.get('image')
        return cleaned_data

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(required=False, widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = ['title','subtitle','location','visited','content','image','draft','publish']

    def clean_publish(self):
        draft = self.cleaned_data.get('draft')
        publish = self.cleaned_data.get('publish')
        today = timezone.now().date()
        if not draft:
            if not publish:
                raise forms.ValidationError("only drafts can be saved without a publish date")
        # if publish < today:
        #     raise forms.ValidationError("publish date can't be in the past")
        return publish

    def clean_location(self):
        location = self.cleaned_data.get('location')
        return location

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"
