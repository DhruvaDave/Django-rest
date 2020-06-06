from rest_framework import serializers
from blog.models import BlogPost,ActivityPost
from account.models import Account

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50
from django.utils import timezone
from django.utils.timezone import activate
# from blog.utils import is_image_aspect_ratio_valid, is_image_size_valid


class BlogPostSerializer(serializers.ModelSerializer):

	username = serializers.SerializerMethodField('get_username_from_author')
	image 	 = serializers.SerializerMethodField('validate_image_url')

	class Meta:
		model = BlogPost
		fields = ['pk', 'title', 'slug', 'body', 'image', 'date_updated', 'username']


	def get_username_from_author(self, blog_post):
		username = blog_post.author.username
		return username

	def validate_image_url(self, blog_post):
		image = blog_post.image
		new_url = image.url
		if "?" in new_url:
			new_url = image.url[:image.url.rfind("?")]
		return new_url




class ActivityPostSerializer(serializers.ModelSerializer):

	userid = serializers.SerializerMethodField('get_userid_from_author')
	real_name = serializers.SerializerMethodField('get_username_from_author')
	# all_activities = serializers.SerializerMethodField('get_activities')
	# all_activities = serializers.SerializerMethodField('to_representation')

	class Meta:
		model = ActivityPost
		# fields = ['pk', 'title', 'slug', 'start_time', 'end_time', 'username']
		fields = ['real_name','userid' ]


	def get_username_from_author(self, activity_post):
		real_name = activity_post.author.username
		return real_name

	def get_userid_from_author(self, activity_post):
		userid = activity_post.author.id
		return userid

	# def get_activities(self, instance):
	# 	print("----instance-----------",instance)
	# 	# user = str(instance['user'])
    #     # date = datetime.datetime.strptime(org_date, "%Y-%m-%d")
    #     # month = date.month
    #     # year = date.year
	# 	# user = instance['author']
	# 	# events = settings.AUTH_USER_MODEL.objects.filter(id=user)
	# 	print("---settings.AUTH_USER_MODEL----", Account)
	# 	print("--- Account----", Account.objects)
	# 	events = Account.objects.all()
	# 	print("--------events----",events)
	# 	event_serializer = UserSerializer(events, many=True)
	# 	# event_serializer = UserSerializer(events)

	# 	print("---------event_serializer-------",event_serializer)
	# 	print("---------event_serializer------data------",event_serializer.data)
	# 	return event_serializer.data

	def to_representation(self,obj):  
		rep= super(ActivityPostSerializer,self).to_representation(obj)  
		# print("--------rep----------",rep,"======ob--------",obj.author)
		# print("------------ALLL--------------",[ customer for customer in ActivityPost.objects.filter(author=obj.author).distinct('author')]  )
		# print("------------ALLL--------------",[ customer for customer in ActivityPost.objects.order_by('author').distinct()]  )
		all_data = [ customer for customer in ActivityPost.objects.filter(author=obj.author).distinct()]  
		temp = []
		to_tz = timezone.get_default_timezone()
		for j in all_data:
			# print("------------start----",j.start_time)
			temp.append({'start_time':j.start_time,'end_time':j.end_time})
			timezone_info = j.start_time.astimezone(to_tz).strftime("%Z")

		print("--------temp--------",timezone_info)
		rep['tz'] = timezone_info
		rep['activity_periods'] = temp
		 
		print("-------------rep-------AFTER",rep)
		return rep  

# class UserSerializer(serializers.ModelSerializer):
# 	# author = ActivityPostSerializer(many=True)
# 	# print("-------author------",author)
# 	class Meta:
# 		model = Account
# 		fields = ['password' ]
# 		# exclude = []


class BlogPostUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

	def validate(self, blog_post):
		try:
			title = blog_post['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			body = blog_post['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
			
			image = blog_post['image']
			url = os.path.join(settings.TEMP , str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			# if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
			# 	os.remove(url)
			# 	raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			# if not is_image_aspect_ratio_valid(url):
			# 	os.remove(url)
			# 	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
		except KeyError:
			pass
		return blog_post

class ActivityPostUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = ActivityPost
		fields = ['title', 'start_time', 'end_time']

	def validate(self, activity_post):
		try:
			title = activity_post['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			start_time = activity_post['start_time']
			end_time = activity_post['end_time']
			if end_time < start_time:
				raise serializers.ValidationError({"response": "End time is grater than start time. Please enter valid end time."})
			
		except KeyError:
			pass
		return activity_post

class BlogPostCreateSerializer(serializers.ModelSerializer):


	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image', 'date_updated', 'author']


	def save(self):
		
		try:
			image = self.validated_data['image']
			title = self.validated_data['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			body = self.validated_data['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
			
			blog_post = BlogPost(
								author=self.validated_data['author'],
								title=title,
								body=body,
								image=image,
								)

			url = os.path.join(settings.TEMP , str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			if not is_image_aspect_ratio_valid(url):
				os.remove(url)
				raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
			blog_post.save()
			return blog_post
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})


class ActivityPostCreateSerializer(serializers.ModelSerializer):


	class Meta:
		model = ActivityPost
		fields = ['title', 'start_time', 'end_time', 'author']


	def save(self):
		
		try:
			start_time = self.validated_data['start_time']
			end_time = self.validated_data['end_time']
			title = self.validated_data['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			start_time = self.validated_data['start_time']
			end_time = self.validated_data['end_time']
			if end_time < start_time:
				raise serializers.ValidationError({"response": "End time is grater than start time. Please enter valid end time.  "})
			
			activity_post = ActivityPost(
								author=self.validated_data['author'],
								title=title,
								start_time=start_time,
								end_time=end_time,
								)

			
			activity_post.save()
			return activity_post
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a title, and some content."})








