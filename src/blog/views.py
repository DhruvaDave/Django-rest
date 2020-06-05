from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from blog.models import BlogPost, ActivityPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm, CreateActivityPostForm, UpdateActivityPostForm

from account.models import Account


def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()

	context['form'] = form
	print("------blog-------context------",context)

	return render(request, "blog/create_blog.html", context)


def create_activity_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateActivityPostForm(request.POST or None, request.FILES or None)
	print("-----------valdi-----------",form.is_valid())
	print("-----------valdi-----------",form.errors)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		print("------------asave------")
		form = CreateActivityPostForm()

	context['form'] = form
	print("--------CreateActivityPostForm---contexct------------",context)

	return render(request, "blog/create_activity.html", context)




def detail_blog_view(request, slug):

	context = {}

	blog_post = get_object_or_404(BlogPost, slug=slug)
	context['blog_post'] = blog_post

	return render(request, 'blog/detail_blog.html', context)


def detail_activity_view(request, slug):

	context = {}

	activity_post = get_object_or_404(BlogPost, slug=slug)
	context['activity_post'] = activity_post

	return render(request, 'blog/detail_activity.html', context)

def edit_blog_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse("You are not the author of that post.")

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj

	form = UpdateBlogPostForm(
			initial = {
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,
			}
		)

	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)

def edit_activity_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	activity_post = get_object_or_404(BlogPost, slug=slug)

	if activity_post.author != user:
		return HttpResponse("You are not the author of that post.")

	if request.POST:
		form = UpdateActivityPostForm(request.POST or None, request.FILES or None, instance=activity_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			activity_post = obj

	form = UpdateActivityPostForm(
			initial = {
					"title": activity_post.title,
					"start_time": activity_post.start_time,
					"end_time": activity_post.end_time,
			}
		)

	context['form'] = form
	return render(request, 'blog/edit_activity.html', context)


def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) | 
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))	


# def get_activity_queryset(query=None):
# 	queryset = []
# 	queries = query.split(" ") # python install 2019 = [python, install, 2019]
# 	for q in queries:
# 		posts = ActivityPost.objects.filter(
# 				Q(title__icontains=q) | 
# 				Q(body__icontains=q)
# 			).distinct()

# 		for post in posts:
# 			queryset.append(post)

# 	return list(set(queryset))	
