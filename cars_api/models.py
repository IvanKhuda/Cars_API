from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='published')


class Car(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    price = models.IntegerField()
    mileage = models.IntegerField()
    fuel = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    engine = models.CharField(max_length=50)
    body_stile = models.CharField(max_length=50)
    exterior_color = models.CharField(max_length=50)
    interior_color = models.CharField(max_length=50)
    on_sale = models.BooleanField()
    publish = models.DateTimeField(default=timezone.localtime)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=250,
                                null=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    slug = models.SlugField(max_length=200,
                            unique_for_date='publish')

    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ('-publish', '-created')
        verbose_name_plural = "cars"

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse('cars_api:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

