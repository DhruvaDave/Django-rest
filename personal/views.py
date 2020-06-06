from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from blog.views import get_blog_queryset,get_activity_queryset
from blog.models import BlogPost

BLOG_POSTS_PER_PAGE = 10
ACTIVITY_POSTS_PER_PAGE = 10

def home_screen_view(request):
	
	context = {}

	query = ""
	query = request.GET.get('q', '')
	context['query'] = str(query)
	print("home_screen_view: " + str(query))

	blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	activity_posts = sorted(get_activity_queryset(query), key=attrgetter('start_time'), reverse=True)
	# Pagination
	page = request.GET.get('page', 1)
	# blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	activity_posts_paginator = Paginator(activity_posts, ACTIVITY_POSTS_PER_PAGE)

	try:
		# blog_posts = blog_posts_paginator.page(page)
		activity_posts = activity_posts_paginator.page(page)
	except PageNotAnInteger:
		# blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
		activity_posts = activity_posts_paginator.page(ACTIVITY_POSTS_PER_PAGE)

	except EmptyPage:
		# blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)
		activity_posts = activity_posts_paginator.page(activity_posts_paginator.num_pages)

	# context['blog_posts'] = blog_posts

	print("----------------last-------activity_posts---------",activity_posts)
	context['activity_posts'] = activity_posts

	return render(request, "personal/home.html", context)
