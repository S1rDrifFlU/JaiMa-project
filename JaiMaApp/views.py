from .models import BlogPost, Like, Comment
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse

from django.contrib.auth import login, authenticate,logout
from .forms import CommentForm, SignUpForm, SignInForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import BlogPost
from .forms import BlogPostForm

def home(request):
    posts = BlogPost.objects.all()

    for post in posts:
        # Check if the request user is the author of each post
        post.is_author = post.author == request.user

        # Retrieve likes and comments for each post
        post.likes = Like.objects.filter(post=post).count()
        post.comments = Comment.objects.filter(post=post).count()

    return render(request, 'JaiMaApp/home.html', {'posts': posts})

@login_required
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
    blog_posts = BlogPost.objects.filter(author=request.user).prefetch_related('like_set', 'comment_set')

    context = {
        'username': username,
        'blog_posts': blog_posts,
    }

    return render(request, 'JaiMaApp/user_profile.html', context)

@login_required
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
    data = {'result': 'success', 'posts': [{'id': post.id, 'title': post.title} for post in posts]}
    return JsonResponse(data)

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Retrieve likes and comments for the post
    likes = Like.objects.filter(post=post)
    comments = Comment.objects.filter(post=post)
    
    return render(request, 'JaiMaApp/post_detail.html', {'post': post, 'likes': likes, 'comments': comments})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm()

    return render(request, 'JaiMaApp/post_form.html', {'form': form})



@login_required
def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        form = BlogPostForm(request.POST,request.FILES, instance=post)
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

@login_required
def set_like(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    existing_like = Like.objects.filter(user=request.user, post=post).first()

    if existing_like:
        existing_like.delete()
    else:
        Like.objects.create(user=request.user, post=post)

    referring_page = request.META.get('HTTP_REFERER')
    
    # Use a default URL in case the referring page is not available
    redirect_url = referring_page or reverse('home')

    return redirect(redirect_url)

def post_comments(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, 'JaiMaApp/post_comments.html', {'post': post, 'comments': comments})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_comments', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'JaiMaApp/add_comment.html', {'form': form, 'post': post})