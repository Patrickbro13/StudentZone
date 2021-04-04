from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
import math
from django.db.models import Count, F, Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.forms.forms import Form
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.models import Contact, PostComment
from blog.forms import NewCommentForm


def home(request):
    allPosts = []
    catprods = Post.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Post.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + math.ceil((n / 4) - (n // 4))
        allPosts.append([prod, range(1, nSlides), nSlides])
    params = {'allPosts': allPosts}
    return render(request, 'blog/home.html', params)
    # context = {
    #   'posts': Post.objects.all()
    # }
    # return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'price', 'prod_img', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'price', 'prod_img', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# def contact(request):
#     return render(request, 'blog/contact.html', {'title': 'About'})

def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'blog/contact.html', {'thank': thank})
# def contact(request):
#     if request.method=="POST":
#         name = request.POST.get('name', '')
#         email = request.POST.get('email', '')
#         message = request.POST.get('message', '')
#         contact = Contact(name=name, email=email, message=message)
#         contact.save()
#     return render(request, 'blog/contact.html')


def temp(request):
    allPosts = []
    catprods = Post.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Post.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + math.ceil((n / 4) - (n // 4))
        allPosts.append([prod, range(1, nSlides), nSlides])
    params = {'allPosts': allPosts}
    return render(request, 'blog/temp.html', params)


class SearchResultView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/search_results.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')

        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query))
        return posts


def Bookmark(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.bookmark.filter(id=request.user.id).exists():
        post.bookmark.remove(request.user)
    else:
        post.bookmark.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class BookmarkView(ListView):
    model = Post
    template_name = 'blog/bookmark.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return (Post.objects.filter(bookmark=self.request.user))


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        post_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        bookmarked = False
        if post_connected.bookmark.filter(id=self.request.user.id).exists():
            bookmarked = True
        data['post_is_bookmarked'] = bookmarked
        comments_connected = PostComment.objects.filter(post_connected = self.get_object()).order_by('date_posted')
        data['content'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)
        return data
    
    def post(self, request, *args, **kwargs):
        new_comment = PostComment(content = request.POST.get('content'), author = self.request.user, post_connected = self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
