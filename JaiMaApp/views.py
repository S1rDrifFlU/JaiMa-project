from .models import BlogPost
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse

from django.contrib.auth import login, authenticate,logout
from .forms import SignUpForm, SignInForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import BlogPost
from .forms import BlogPostForm

@login_required
def home(request):
    posts = BlogPost.objects.all()

    # Check if the request user is the author of each post
    for post in posts:
        post.is_author = post.author == request.user

    return render(request, 'JaiMaApp/home.html', {'posts': posts})

def profile(request):
    # Add logic to fetch user profile information
    return render(request, 'JaiMaApp/profile.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home or any other page after signup
    else:
        form = SignUpForm()
    return render(request, 'JaiMaApp/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change this line to redirect to the 'home' view
    else:
        form = AuthenticationForm()
    return render(request, 'JaiMaApp/signin.html', {'form': form})

@login_required
def user_profile(request):
    # Retrieve the user's username
    username = request.user.username

    # Retrieve the user's blog posts
    blog_posts = BlogPost.objects.filter(author=request.user)

    context = {
        'username': username,
        'blog_posts': blog_posts,
    }

    return render(request, 'JaiMaApp/user_profile.html', context)

def signout(request):
    logout(request)
    return redirect('home')

def search_posts(request):
    query = request.GET.get('q', '')
    # Perform a case-insensitive search for blog posts with titles containing the query
    posts = BlogPost.objects.filter(title__icontains=query)
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'JaiMaApp/search_posts.html', context)

def search_posts_live(request):
    query = request.GET.get('q', '')
    posts = BlogPost.objects.filter(title__icontains=query)
    data = {'result': 'success', 'posts': [{'title': post.title} for post in posts]}
    return JsonResponse(data)

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'JaiMaApp/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'JaiMaApp/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'JaiMaApp/post_form.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'JaiMaApp/post_confirm_delete.html', {'post': post})