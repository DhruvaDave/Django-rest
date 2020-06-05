from django import forms

from blog.models import BlogPost,ActivityPost


class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

class CreateActivityPostForm(forms.ModelForm):

	class Meta:
		model = ActivityPost
		fields = ['title', 'start_time', 'end_time']


class UpdateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

	def save(self, commit=True):
		blog_post = self.instance
		blog_post.title = self.cleaned_data['title']
		blog_post.body = self.cleaned_data['body']

		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']

		if commit:
			blog_post.save()
		return blog_post

class UpdateActivityPostForm(forms.ModelForm):

	class Meta:
		model = ActivityPost
		fields = ['title', 'start_time', 'end_time']

	def save(self, commit=True):
		activity_post = self.instance
		activity_post.title = self.cleaned_data['title']
		activity_post.start_time = self.cleaned_data['start_time']
		activity_post.end_time = self.cleaned_data['end_time']

		
		if commit:
			activity_post.save()
		return activity_post