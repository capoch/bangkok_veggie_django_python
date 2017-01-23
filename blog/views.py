from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post
# Create your views here.

#CRUD for blogs
def posts_create(request):
    form = PostForm(request.POST or None)
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

def posts_detail(request,pk):
    post = get_object_or_404(Post,id=pk)
    context = {
        "post":post,
    }
    return render(request,'post_detail.html',context)


def posts_list(request):
    queryset_list = Post.objects.all()
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
    }
    return render(request,'post_list.html',context)



def posts_edit(request, pk=None):
    post = get_object_or_404(Post,id=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Item saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        }
    return render(request,'post_form.html', context)


def posts_delete(request, pk=None):
    post = get_object_or_404(Post,id=pk)
    post.delete()
    messages.success(request,"Successfully deleted that shit")
    return redirect("posts:home")
