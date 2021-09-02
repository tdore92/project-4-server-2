from django.urls import path
from .views import ItemDetailView, ItemListView, CommentListView, CommentDetailView

urlpatterns = [
    path('', ItemListView.as_view()),
    path('<int:pk>/', ItemDetailView.as_view()),
    path('<int:item_pk>/comments/', CommentListView.as_view()),
    path('<int:_item_pk>/comments/<int:comment_pk>/', CommentDetailView.as_view())
]
