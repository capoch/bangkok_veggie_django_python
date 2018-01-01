from urllib.parse import quote

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.template import Context, loader
from django.template.loader import get_template

from .forms import PostForm, LocationForm, ImageForm, ContactForm
from .models import Post, Location, Image
from .utils import count_words, get_read_time
from comments.models import Comment
# Create your views here.

#Register new location
def location_create(request):

    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=2)

    if not request.user.is_authenticated:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
        raise PermissionDenied

    if request.method == 'POST':

        form = LocationForm(request.POST or None, request.FILES or None)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        print("Request Files: ")
        print(request.FILES)
        print("Formset: ")
        print(formset)
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            instance.save()
            print("Cleaned Data: ")
            print(formset.cleaned_data)
            for image_form in formset.cleaned_data:
                image = image_form.get('image')
                photo = Image(location = instance, image=image)
                photo.save()

            messages.success(request,"Successfully created")

            return HttpResponseRedirect(instance.get_absolute_url())

    else:
        form = LocationForm()
        formset = ImageFormSet()
        print("Formset: ")
        print(formset)

    if form.errors:
        messages.error(request,"Nope, not created")

    context = {
        "form": form, "formset": formset,
        }

    return render(request,'location_form.html', context)

def location_detail(request,slug):
    location = get_object_or_404(Location,slug=slug)
    content_type = ContentType.objects.get_for_model(Location)
    obj_id = location.id
    comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
    images = Image.objects.filter(location=location)
    context = {
        "name": location.name,
        "location": location,
        "comments": comments,
        "images": images,
    }
    return render(request,'location_detail.html',context)

def location_list(request):
    today = timezone.now().date()
    queryset_list = Location.objects.all()
    #Search Function
    search = request.GET.get('q')
    if search:
        queryset_list=queryset_list.filter(
        Q(name__icontains=search)|
        Q(suburb__icontains=search)|
        Q(loc_type__icontains=search)|
        Q(cuisine__icontains=search)
        ).distinct()
    #Pagination
    paginator = Paginator(queryset_list, 10) # Show 10 contacts per page
    page_request_var = 'abc'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title":"BangkokVeg - Streetfood Dilemma",
        "object_list": queryset,
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request,'location_list.html',context)

def location_edit(request, slug=None):
    if not request.user.is_authenticated:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
        raise PermissionDenied
    location = get_object_or_404(Location,slug=slug)
    form = LocationForm(request.POST or None, request.FILES or None, instance = location)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Item saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        }
    return render(request,'location_form.html', context)


#CRUD for blogs
def posts_create(request):
    if not request.user.is_authenticated:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
        raise PermissionDenied
    form = PostForm(request.POST or None, request.FILES or None, initial={"publish": timezone.now().date()})
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    elif form.errors:
        messages.error(request,"Nope, not created")
    context = {
        "form": form,
        }
    return render(request,'post_form.html', context)

def posts_detail(request,slug):
    post = get_object_or_404(Post,slug=slug)
    if not post.publish or post.publish > timezone.now().date() or post.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            if not post.user == request.user:
                raise PermissionDenied
    content_type = ContentType.objects.get_for_model(Post)
    obj_id = post.id
    comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
    context = {
        "title": post.title,
        "post": post,
        "comments": comments,
    }
    return render(request,'post_detail.html',context)


def posts_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.published()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    #Search Function
    search = request.GET.get('q')
    if search:
        queryset_list=queryset_list.filter(
        Q(title__icontains=search)|
        Q(content__icontains=search)|
        Q(user__first_name__icontains=search)|
        Q(user__last_name__icontains=search)
        ).distinct()
    #Pagination
    paginator = Paginator(queryset_list, 10) # Show 10 contacts per page
    page_request_var = 'abc'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title":"BangkokVeg - Streetfood Dilemma",
        "object_list": queryset,
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request,'post_list.html',context)



def posts_edit(request, slug=None):
    if not request.user.is_authenticated:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
        raise PermissionDenied
    post = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Item saved")
        print(instance)
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        }
    return render(request,'post_form.html', context)


def posts_delete(request, slug=None):
    if not request.user.is_authenticated:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
        raise PermissionDenied
    post = get_object_or_404(Post,slug=slug)
    post.delete()
    messages.success(request,"Successfully deleted that shit")
    return redirect('about.html')

def about(request):
    context = []
    return render(request,'about.html', context)

def vdict(request):
    context = []
    return render(request,'dict.html', context)

def thai_dishes(request):
    context = []
    return render(request,'thai_dishes.html', context)

def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "contact_form@bangkokveggie.com",
                ['angela_zgr@yahoo.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()

            return redirect('posts:contact')

    return render(request, 'contact.html', {
        'form': form_class,
    })
