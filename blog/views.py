from django.contrib import messages
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
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "title":"Liste mit Titel und Shice",
    }
    return render(request,'index.html',context)

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
