from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(
        auto_now_add=True
    )  # auto_now_add=True data insert time can't change
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Users save in DB will have unique "ID" e.t.c 1,2,3...
    # User 對應創建事件的 user

    def __str__(self):
        return self.title  # show title in admin page
