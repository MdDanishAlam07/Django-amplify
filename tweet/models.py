from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tweet(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.TextField(max_length=500)
  photo = models.ImageField(upload_to='tweets/photos/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f"{self.user.username}: {self.text[:50]}"
  



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name