from django.urls import path, include
from newsfeed.views import create_post,PostListView,post_delete,search_posts

urlpatterns=[

    path('create_post',create_post, name='create_post'),
    path('',PostListView.as_view(),name='home'),
	path('post/<int:pk>/delete/', post_delete, name='post-delete'),
    path('search_posts/', search_posts, name='search_posts'),

    

]
