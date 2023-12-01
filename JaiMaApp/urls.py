from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import add_comment, home, post_comments, profile, set_like,signin,signup,signout,user_profile,search_posts,search_posts_live,post_create,post_delete,post_detail,post_edit

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    # path('signout/', signout, name='signout'),
    path('user_profile/', user_profile, name='user_profile'),
    path('search/', search_posts, name='search_posts'),  
    path('live_search/', search_posts_live, name='search_posts_live'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/new/', post_create, name='post_create'),
    path('post/<int:pk>/edit/', post_edit, name='post_update'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    path('signout', signout,name="signout"),
    path('set_like/<int:post_id>/', set_like, name='set_like'),
    path('post/<int:pk>/comments/', post_comments, name='post_comments'),
    path('post/<int:post_id>/add_comment/', add_comment, name='add_comment'),
    # Add other URLs as needed
]
