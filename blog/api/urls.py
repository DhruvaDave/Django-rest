from django.urls import path
from blog.api.views import(
	api_detail_blog_view,
	api_update_blog_view,
	api_delete_blog_view,
	api_create_blog_view,
	
	api_is_author_of_blogpost,

	api_detail_activity_view,
	api_update_activity_view,
	api_delete_activity_view,
	api_create_activity_view,
	api_is_author_of_activitypost,


	ApiBlogListView,
	ApiActivityListView,
	# ApiUserListView
)

app_name = 'blog'

urlpatterns = [
	path('<slug>/', api_detail_blog_view, name="detail"),
	path('<slug>/update', api_update_blog_view, name="update"),
	path('<slug>/delete', api_delete_blog_view, name="delete"),
	path('create', api_create_blog_view, name="create"),
	path('list', ApiBlogListView.as_view(), name="list"),
	path('<slug>/is_author', api_is_author_of_blogpost, name="is_author"),

	path('activity/<slug>/', api_detail_activity_view, name="detail_activity"),
	path('activity/<slug>/update', api_update_activity_view, name="update_activity"),
	path('activity/<slug>/delete', api_delete_activity_view, name="delete_activity"),
	path('activity/create', api_create_activity_view, name="create_activity"),
	path('activity/list', ApiActivityListView.as_view(), name="list_activity"),
	path('activity/<slug>/is_author', api_is_author_of_activitypost, name="is_author_activity"),
]