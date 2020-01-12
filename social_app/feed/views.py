from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import User
from django.template.loader import render_to_string
from .models import Post
import logging

logger = logging.getLogger(__name__)



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'feed/home.html',  context)


def about(request):

    return render(request, 'feed/about.html',  {'title': 'Now You Know - about'})

class PostListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'feed/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #checking if the user trying to update a post is the original author of the post, if so, return True
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def post_detail(request, id):
    post = Post.objects.get(id=id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes':post.total_likes(),
    }

    return render(request, 'feed/post_detail.html', context)




def like_post(request):
    # post_id = request.POST["post_id"]
    # post = Post.objects.get(pk=post_id)
    # user = request.user
    # return HttpResponseRedirect("")
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    logger.error("!!!!")
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        is_liked = True
    # user = request.user
    # post.toggle_like(user)

    return HttpResponseRedirect(post.get_absolute_url())



def userprofile(request, username):
    userarr = User.objects.filter(username=username)
    user = userarr.first()
    posts = Post.objects.filter(author = user.id)

    context = {"posts": posts}

    return render(request, 'feed/home.html', context)


class UserPostList(ListView):
    model = User

    slug_field = "username"
    slug_url_kwarg = "username"
