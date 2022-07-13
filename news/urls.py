from django.urls import path
from .views import (
    NewsDetailView,
    NewsUpdateView,
    NewsDeleteView,
    AddPostView,
    CategoryView,
    LikeView
)

urlpatterns = [
    path('add_post', AddPostView.as_view(), name='add_post'),
    path('<int:pk>', NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/update', NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete', NewsDeleteView.as_view(), name='news-delete'),
    path('category/<str:slug>', CategoryView.as_view(), name='category'),
    path('like/<int:pk>', LikeView, name='like_post')
]
