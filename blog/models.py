from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdown_deux import markdown

from .utils import get_read_time
# Create your models here.

CUISINE = (
    ('vegetarian', 'vegetarian'),
    ('thai', 'thai'),
    ('european', 'european'),
    ('chinese', 'chinese'),
    ('korean', 'korean'),
    ('fusion', 'fusion'),
    ('indian', 'indian'),
    ('french', 'french'),
    ('italian', 'italian'),
    ('mexican', 'mexican'),
    ('american', 'american'),
    ('vietnamese', 'vietnamese'),
    ('other', 'other'),
)

LOCATION_TYPE = (
    ('Streetfood', 'Streetfood'),
    ('Cheap Restaurant', 'Cheap Restaurant'),
    ('Restaurant', 'Restaurant'),
    ('Fine Dining', 'Fine Dining'),
    ('Delivery Only', 'Delivery Only'),
)

class Location(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(null=True, blank=True, max_length=250)
    suburb = models.CharField(null=True, blank=True, max_length=250)
    cuisine = models.CharField(max_length=40, choices = CUISINE)
    loc_type = models.CharField(null=True, blank=True, max_length=40, choices = LOCATION_TYPE)
    maplink = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    slug =  models.SlugField(unique=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    delivery_avaiable = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ['-rating','name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('posts:detail_location', kwargs = {"slug": self.slug}) #namespace:url_name

def get_image_filename(instance, filename):
    title = instance.location.name
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)

def upload_location(obj, filename):
    return "%s/%s" %(obj.slug,filename)

class Image(models.Model):
    location = models.ForeignKey(Location, default=None)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')


    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)


class PostManager(models.Manager):
    def published(self, *args, **kwargs):
        return self.filter(draft=False).filter(publish__lte=timezone.now())



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=250)
    subtitle = models.CharField(null=True, blank=True, max_length=250)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    visited = models.DateField(auto_now=False,auto_now_add=False, null=True, blank=True)
    slug =  models.SlugField(unique=True)
    image = models.ImageField(upload_to = upload_location, null=True, blank=True, height_field="image_height", width_field="image_width")
    image_height = models.IntegerField(default=0)
    image_width = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=True)
    publish = models.DateField(auto_now=False,auto_now_add=False, null=True, blank=True)
    read_time = models.IntegerField(null=True, blank=True, default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    class Meta:
        ordering = ['-publish','-timestamp','-updated']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs = {"slug": self.slug}) #namespace:url_name

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))

class LocationImage(models.Model):
    property = models.ForeignKey(Location, related_name='location_images')
    image = models.ImageField()

class PostImage(models.Model):
    property = models.ForeignKey(Post, related_name='blog_images')
    image = models.ImageField()

def create_slug(instance, new_slug=None):
    if type(instance) == Post:
        slug = slugify(instance.title)
    elif type(instance) == Location:
        slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    if type(instance) == Post:
        qs = Post.objects.filter(slug=slug).order_by('id')
    elif type(instance) == Location:
        qs = Location.objects.filter(slug=slug).order_by('id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        instance.read_time = get_read_time(html_string)

pre_save.connect(pre_save_post_receiver, sender=Post)

def pre_save_location_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_location_receiver, sender=Location)
# pre_save.connect(pre_save_location_receiver, sender=Image)
