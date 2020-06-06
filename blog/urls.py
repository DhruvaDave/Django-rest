from django.urls import path
from blog.views import(

	create_blog_view,
	detail_blog_view,
	edit_blog_view,

	create_activity_view,
	detail_activity_view,
	edit_activity_view,

)

app_name = 'blog'

urlpatterns = [
	path('create/', create_blog_view, name="create"),
	path('<slug>/', detail_blog_view, name="detail"),
	path('<slug>/edit', edit_blog_view, name="edit"),
	path('activity/create/', create_activity_view, name="create_activity"),
	path('activity/<slug>/', detail_activity_view, name="detail_activity"),
	path('activity/<slug>/edit', edit_activity_view, name="edit_activity"),
]