from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from newsfeed.forms import NewPostForm
from newsfeed.models import Post
from django.contrib.auth.decorators import login_required
from users.models import User

# Create your views here.

@login_required
def create_post(request):
	user = request.user
	if request.method == "POST":
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			data.user_name = user
			data.save()
			messages.success(request, f'Posted Successfully')
			return redirect('home')
	else:
		form = NewPostForm()
	return render(request, 'newsfeed/create_post.html', {'form':form})


class PostListView(ListView):
	model = Post
	template_name = 'newsfeed/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5



@login_required
def post_delete(request, pk):
	post = Post.objects.get(pk=pk)
	if request.user== post.user_name:
		Post.objects.get(pk=pk).delete()
	return redirect('home')


@login_required
def search_posts(request):
	query = request.GET.get('p')
	object_list = Post.objects.filter(tags__icontains=query)
	context ={
		'posts': object_list,
	}
	return render(request, "newsfeed/search_posts.html", context)