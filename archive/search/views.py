from django.shortcuts import render
from .models import User, Post
from .filters import *

def index(request):
	my_filter = UserFilter(request.GET, queryset = Post.objects.filter(display = True))
	post_list = my_filter.qs

	context = {
		'my_filter': my_filter,
		'post_list': post_list,
	}

	return render(request, 'search/index.html', context)
