from django.db import models
# Create your models here.


class Item(models.Model):

    name = models.CharField(max_length=50)

    type = models.CharField(max_length=50)

    diet = models.CharField(max_length=50)

    size = models.CharField(max_length=50)

    description = models.CharField(max_length=500)

    price = models.FloatField(default=0)

    image = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.name}'

class Comment(models.Model):
    content = models.TextField(max_length=250)
    item = models.ForeignKey(
        Item,
        related_name='comments',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='comments',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Comment {self.id} on {self.item}'
