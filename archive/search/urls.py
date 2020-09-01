from django.urls import path
from . import views

# app_name = 'search'
urlpatterns = [
	path('', views.index, name='index'),
	# path('<slug:username>/', views.results, name='username'),
	# path('<slug:username>/results/', views.results, name='results'),
	# path('all/', views.all, name='all'),
] 