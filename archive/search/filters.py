import django_filters
from .models import *

class UserFilter(django_filters.FilterSet):
	artist = django_filters.CharFilter(lookup_expr='icontains')
	song = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = Post
		fields = ['user', 'artist', 'song']
