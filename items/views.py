
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Comment, Item
from .serializers import ItemSerializers, PopulatedItemSerializer, CommentSerializer

# Create your views here.
class ItemListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        items = Item.objects.all()
        serialized_items = ItemSerializers(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)

    def post(self, request):
        new_item = ItemSerializers(data=request.data)
        if new_item.is_valid():
            new_item.save()
            return Response(new_item.data, status=status.HTTP_201_CREATED)
        return Response(new_item.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ItemDetailView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_item(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise NotFound()

    def get(self, _request, pk):
        item = self.get_item(pk=pk)
        serialized_item = PopulatedItemSerializer(item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)

    def delete(self, _request, pk):
        item_to_delete = self.get_item(pk=pk)
        item_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        item_to_update = self.get_item(pk=pk)
        updated_item = ItemSerializers(item_to_update, data=request.data)
        if updated_item.is_valid():
            updated_item.save()
            return Response(updated_item.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_item.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CommentListView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, item_pk):
        request.data['item'] = item_pk
        request.data['owner'] = request.user.id
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CommentDetailView(APIView):

    def delete(self, request, _item_pk, comment_pk):
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            if comment_to_delete.owner != request.user:
                raise PermissionDenied()
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound()
