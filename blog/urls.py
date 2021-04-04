from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchResultView
)
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('temp/', views.temp, name='temp'),
    path('post/search/', SearchResultView.as_view(), name='search-result'),
    path('post-bookmark/<int:pk>/', views.Bookmark, name='post-bookmark'),
    path('post/bookmark/', views.BookmarkView.as_view(), name='bookmark-post'),
]
