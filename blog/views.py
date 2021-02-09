from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView, DetailView, CreateView,
                                  UpdateView, DeleteView,
                                  )
from django.utils import timezone
from blog.forms import PostForm
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


########## POSTS/DRAFT FORM VIEW ##########


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by("-published_date")

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "blog/post_detail.html"
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "blog/post_detail.html"
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")

class DraftListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "blog/post_list.html"
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.publish()
    return redirect("post_detail", pk = pk)