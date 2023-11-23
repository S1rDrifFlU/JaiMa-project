from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import home, profile,signin,signup,signout,user_profile,search_posts,search_posts_live,post_create,post_delete,post_detail,post_edit

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
    path('signout/', auth_views.LogoutView.as_view(next_page='home'), name='signout'),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    # Add other URLs as needed
]
