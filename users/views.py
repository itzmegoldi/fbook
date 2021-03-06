from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from users.forms import RegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile,FriendRequest
from django.http import HttpResponseRedirect
import random
from users.models import User
from django.db.models import Q
from newsfeed.models import Post
from django.contrib import messages


# Create your views here.
def RegistrationView(request): 
	form=RegistrationForm(request.POST)
	if form.is_valid():
		form.save()
		phone=form.cleaned_data.get('phone')
		password1=form.cleaned_data.get('password1')
		context={'form':form,'msg':'User succesfully registerd,'}
		return redirect('login')
			# return redirect('home')
	else:
		form=RegistrationForm()
		msg='the form is invalid'
		context={'form':form,'msg':msg}
	form=RegistrationForm()
	context={'form':form}
	return render(request,'users/register.html',context)

def loginView(request):
	if request.user.is_authenticated:
		return render(request, 'newsfeed/home.html')
	if request.method=='GET':
		return render(request, 'users/login.html', {})
	else:
		phone = request.POST['phone']
		password = request.POST['password']
		user = authenticate(request, phone=phone, password=password)
		if user is not None :
			login(request, user)
			return redirect('home')
		else:
			msg='Invalid phone or Password'
			return render(request, 'users/login.html', {'msg':msg})
def logout_view(request):
	logout(request)
	return render(request,'users/logout.html')

def must_authenticate(request):
	return render(request,'registration/must_authenticate.html')

@login_required
def users_list(request):
	users = Profile.objects.exclude(user=request.user)
	sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
	my_friends = request.user.profile.friends.all()
	sent_to = []
	friends = []
	for user in my_friends:
		friend = user.friends.all()
		for f in friend:
			if f in friends:
				friend = friend.exclude(user=f.user)
		friends += friend
	for i in my_friends:
		if i in friends:
			friends.remove(i)
	if request.user.profile in friends:
		friends.remove(request.user.profile)
	random_list = random.sample(list(users), min(len(list(users)), 10))
	for r in random_list:
		if r in friends:
			random_list.remove(r)
	friends += random_list
	for i in my_friends:
		if i in friends:
			friends.remove(i)
	for se in sent_friend_requests:
		sent_to.append(se.to_user)
	context = {
		'users': friends,
		'sent': sent_to
	}
	return render(request, "users/users_list.html", context)



@login_required
def send_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user,
			to_user=user)
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

@login_required
def cancel_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(
			from_user=request.user,
			to_user=user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

@login_required
def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	if(FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
		request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
		request_rev.delete()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

@login_required
def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

@login_required
def delete_friend(request, id):
	user_profile = request.user.profile
	friend_profile = get_object_or_404(Profile, id=id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)
	return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))


@login_required
def friend_list(request):
	p = request.user.profile
	friends = p.friends.all()
	context={
	'friends': friends
	}
	return render(request, "users/friend_list.html", context)


def profile_view(request, slug):
	if request.user.is_authenticated:
		p = Profile.objects.filter(slug=slug).first()
		u = p.user
		sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
		rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
		user_posts = Post.objects.filter(user_name=u)

		friends = p.friends.all()

		# is this user our friend
		button_status = 'none'
		if p not in request.user.profile.friends.all():
			button_status = 'not_friend'

			# if we have sent him a friend request
			if len(FriendRequest.objects.filter(
				from_user=request.user).filter(to_user=p.user)) == 1:
					button_status = 'friend_request_sent'

			# if we have recieved a friend request
			if len(FriendRequest.objects.filter(
				from_user=p.user).filter(to_user=request.user)) == 1:
					button_status = 'friend_request_received'

		context = {
			'u': u,
			'button_status': button_status,
			'friends_list': friends,
			'sent_friend_requests': sent_friend_requests,
			'rec_friend_requests': rec_friend_requests,
			'post_count': user_posts.count
		}

		return render(request, "users/profile.html", context)
	else:
		return redirect('login')

@login_required
def edit_profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('edit_profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context ={
		'u_form': u_form,
		'p_form': p_form,
	}
	return render(request, 'users/edit_profile.html', context)

@login_required
def search_users(request):
	query = request.GET.get('q')
	user_list=[]
	object_list = User.objects.filter(Q(phone__icontains=query)|
									  Q(first_name__icontains=query)|
									  Q(last_name__icontains=query))

	friends = request.user.profile.friends.all()
	for f in object_list:
		if f in friends:
			user_list.append(f)
	for f in object_list:
		if f not in friends:
			user_list.append(f)


	context ={
		'users': users_list
	}
	return render(request, "users/search_users.html", context)

