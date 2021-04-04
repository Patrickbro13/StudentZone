from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

Category_choices = (
    ("Books", "Books"),
    ("Reference Notes", "Reference Notes"),
    ("Lab Equipments", "Lab Equipments"),
    ("Electronic Equipments", "Electronic Equipments"),
    ("Sports Equipments", "Sports Equipments"),
    ("Appliances", "Appliances"),
    ("Miscellenous", "Miscellenous")
)


class Post(models.Model):
    title = models.CharField(max_length=100)
    prod_img = models.ImageField(
        default='default_thumbnail.png', upload_to='Product_images')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0.00)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=30, choices=Category_choices, default='Miscellenous')
    
    bookmark = models.ManyToManyField(User, related_name='bookmark')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.prod_img.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.prod_img.path)

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name