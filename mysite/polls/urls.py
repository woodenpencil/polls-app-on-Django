from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
	path('', views.Index_view.as_view(), name='index'),
	path('<int:pk>/', views.Detail_view.as_view(), name='detail'),
	path('<int:pk>/results/', views.Results_view.as_view(), name='results'),
	path('<int:question_id>/vote/', views.vote, name='vote'),
]