from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from users.models import User
from django.template.loader import render_to_string
from .models import Post, Comment
from .forms import CommentForm
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
    paginate_by = 10
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
    comments = Comment.objects.filter(post = post).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method =='POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content=request.POST.get('content')
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            comment.save()

            #return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes':post.total_likes(),
        'comments':comments,
        'comment_form': comment_form,
    }

    if request.is_ajax():
        html = render_to_string('feed/comment_section.html', context, request=request)
        return JsonResponse({'form':html})

    return render(request, 'feed/post_detail.html', context)



@login_required
#@require_http_methods(["POST"])
def like_post(request):
    # post_id = request.POST["post_id"]
    # post = Post.objects.get(pk=post_id)
    # user = request.user
    # return HttpResponseRedirect("")
    logger.error(request.user)
    post_id = request.POST.get("post")
    logger.error(post_id)
    post = get_object_or_404(Post, id=request.POST.get("post"))

    user=request.user

    is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        logger.error("!!!!")
    else:
        post.likes.add(request.user)
        is_liked = True
        logger.error("*****")
    # user = request.user
    # post.toggle_like(user)

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes':post.total_likes(),
    }
    if request.is_ajax():
        logger.error("*** " + str(post.total_likes())+ " ***")
        return JsonResponse({'likes':post.total_likes()})
    #return HttpResponseRedirect(post.get_absolute_url())

def profile(request):
    user= request.user
    posts = Post.objects.filter(author = user.id)

    context = {
        "posts": posts,
        "username": user.username,
        }

    return render(request, 'feed/userprofile.html', context)

def liked_posts(request, username):
    user = User.objects.filter(username=username).first()
    liked_posts = user.likes.all()

    context = {
        "posts": liked_posts,
        "username": username,
        }
    return render(request, 'feed/userprofile.html', context)

def userprofile(request, username):
    userarr = User.objects.filter(username=username)
    user = userarr.first()
    logger.error("YOOOO")
    logger.error(username)
    posts = Post.objects.filter(author = user.id)

    context = {
        "posts": posts,
        "username": user,
        }


    return render(request, 'feed/userprofile.html', context)


class UserPostList(ListView):
    model = User

    slug_field = "username"
    slug_url_kwarg = "username"
