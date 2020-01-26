from django.urls import path
from . import views
from .views import PostListView, PostCreateView, PostDeleteView, PostUpdateView
from django.conf.urls import url

urlpatterns = [
    path('', PostListView.as_view(), name='feed-home'),
    path('profile/', view=views.profile, name='profile'),
    path('liked-posts/', view=views.liked_posts, name='liked_posts'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    url(regex=r'^post/(?P<id>\d+)/$', view=views.post_detail, name="post_detail"),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    url(regex=r"^like/$", view=views.like_post, name="like_post"),
    url(regex=r"^(?P<username>[\w.@+-]+)/$", view=views.userprofile, name='user-posts'),
    path('about/', views.about, name='feed-about'),
]
