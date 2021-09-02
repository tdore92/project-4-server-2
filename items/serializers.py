from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Item, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'

class PopulatedCommentSerializer(CommentSerializer):
    owner = UserSerializer()

class PopulatedItemSerializer(ItemSerializers):
    comments = PopulatedCommentSerializer(many=True)
