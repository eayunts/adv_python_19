from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.db.models import ImageField
#from sorl.thumbnail import ImageField



class Blog(models.Model):
    Name = models.CharField(max_length=100)
    Slug = models.SlugField(max_length=200, unique = True, null=True, blank=True)

    def __str__(self):
        return self.Name


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,related_name='blog_post',default=1)
    Title = models.CharField(max_length=500)
    Author = models.ForeignKey("auth.User",on_delete = models.CASCADE, verbose_name="your name")
    Image = models.ImageField()
    Content = RichTextField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    Slug = models.SlugField(max_length=200, unique = True, null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['Date']

    def __str__(self):
        return self.Title
    
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        value = self.Title
        self.Slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.Image and hasattr(self.Image, 'url'):
            return self.Image.url
    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = RichTextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Like(models.Model):
    user= models.ForeignKey("auth.User",on_delete=models.CASCADE)
    post= models.ForeignKey(Post,on_delete=models.CASCADE)
    value= models.IntegerField(default=0)
    updated_at= models.DateTimeField(auto_now= True)
    
    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")