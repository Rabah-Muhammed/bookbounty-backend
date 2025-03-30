from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["username"] 

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    favorite_genre = models.CharField(max_length=50, blank=True, null=True) 

    def __str__(self):
        return f"{self.user.username}'s Profile"



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)  
    genre = models.CharField(max_length=50)
    publication_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="book_covers/", blank=True, null=True)
    pdf_file = models.FileField(upload_to="book_pdfs/", blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ReadingList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reading_lists")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    
class ReadingListBook(models.Model):
    reading_list = models.ForeignKey(ReadingList, on_delete=models.CASCADE, related_name="books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)  

    class Meta:
        unique_together = ("reading_list", "book")  

    def __str__(self):
        return f"{self.book.title} in {self.reading_list.name}"