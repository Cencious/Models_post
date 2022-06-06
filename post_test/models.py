from operator import truediv
from re import I
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db. models.signals import post_delete, post_save
from django.utils.text import slugify#helps slugyfy the hashtags
from django.urls import reverse
import uuid


#first create all images profile pictures all images videos will be directed to that folder.

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user_id, filename) #returns user that owns the profile

class Tag(models.Model):
    title = models.CharField(max_length=100,verbose_name="Tag")
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1) #al tags should have a tag and unique

    class Meta:
        verbose_name ='Tag'#when one tag
        verbose_name_plural ='Tags'#when with more than ne tag it says tags

    def get_absolute_url(self): #when a user clicks on the tags it takes them to a page with more details.
        return reverse('tags',args=[self.slug])# the name of url is tags, args=[self.slug]to get a particular post.

    def __str__(self):# returns what the user wants.
        return self.title #returns the title of the tag


    def save(self, *args, **kwargs):#method to save the tag
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)# arguments and keyword arguments

class Post(models.Model):#helps keep track of posts
    id = models.UUIDField(primary_key=True,
    default=uuid.uuid4, editable=False) # post should notbe editable, uuid(universally unique identifier)helps generating random objects of 128 bits as ids uniquely.
    picture = models.ImageField(upload_to=user_directory_path, verbose_name="Picture") #allows adding pictures
    caption = models.CharField(max_length=10000, verbose_name="Caption")
    posted = models.DateField(auto_now_add=True)#gets current date and time and appends to the post.
    tags = models.ManyToManyField(Tag, related_name="tags")#creates a relationship parent child.
    user = models.ForeignKey(User, on_delete=models.CASCADE)# if user gets deleted what should be done to their field.
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post-details", args=[str(self.id)])#how to identify the post is the exact post needed, it identifies using id.

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower') #
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

class Stream(models.Model):# when u follow a user it auto streams all they posted.
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    date = models.DateTimeField()#creates date 

    def add_post(sender, instance, *args, **kwargs):#when i follow you iyt add all my post
        post = instance  
        user = post.user# get the variable user and all post of the user u follow.
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:#
            stream = Stream(post=posts, follow=follower, date=post.posted, following=user)
            stream.save()

    #create a signal      
post_save.connect(Stream.add_post, sender=Post)

post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unliked_post, sender=Likes)

post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)  

    
