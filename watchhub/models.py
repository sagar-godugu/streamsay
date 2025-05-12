from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class StreamPlatform(models.Model):
    name=models.CharField(max_length=100)
    about=models.TextField()
    website=models.URLField()
    def __str__(self):
        return self.name

class WatchContent(models.Model):
    title=models.CharField(max_length=100)
    storyline=models.TextField()
    active=models.BooleanField(default=False)
    stream_platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name='watchcontent')
    avg_rating=models.FloatField(default=0)
    total_rating=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class ContentReview(models.Model):
    critic=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    feedback=models.TextField()
    watchcontent=models.ForeignKey(WatchContent,on_delete=models.CASCADE,related_name="reviewcontent")
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.rating)+'-'+self.watchcontent.title
    