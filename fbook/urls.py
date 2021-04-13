"""fbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('newsfeed.urls')),
    path('users/', views.users_list, name='users_list'),
    path('users/<slug>/',views.profile_view, name='profile_view'),
    path('friends/',views.friend_list, name='friend_list'),
	path('users/friend-request/send/<int:id>/',views.send_friend_request, name='send_friend_request'),
	path('users/friend-request/cancel/<int:id>/',views.cancel_friend_request, name='cancel_friend_request'),
    path('users/friend-request/accept/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
	path('users/friend-request/delete/<int:id>/', views.delete_friend_request, name='delete_friend_request'),
	path('users/friend/delete/<int:id>/', views.delete_friend, name='delete_friend'),
	path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('search_users/',views.search_users, name='search_users'),
    path('register',views.RegistrationView,name='register'),
    path('login',views.loginView,name='login'),
    path('logout',views.logout_view,name='logout'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
