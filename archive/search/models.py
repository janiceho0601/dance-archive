from django.db import models
from django.utils import timezone

class User(models.Model):
	username = models.CharField(primary_key=True, max_length=200)
	num_posts = models.IntegerField(default=0)
	num_followers = models.IntegerField(default=0)
	num_following = models.IntegerField(default=0)

	def __str__(self):
		return self.username

	def get_posts(self):
		return self.num_posts

	def get_followers(self):
		return self.num_followers

	def get_following(self):
		return self.num_following

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	url = models.URLField(unique=True)
	display = models.BooleanField(default=False)
	full_caption= models.TextField(blank=True)
	short_caption = models.TextField(blank=True)
	mentions = models.TextField(blank=True)
	hashtags = models.TextField(blank=True)
	song = models.CharField(max_length=200)
	artist = models.CharField(max_length=200)
	thumbnail = models.CharField(unique=True, max_length=200)

	def __str__(self):
		output = self.url 
		return output

	def get_user(self):
		return self.user.username

	def get_music(self):
		output = self.artist + "\n" + self.song
		return output