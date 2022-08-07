from django.db import models
from django.contrib.auth.models import User
from unidecode import unidecode
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image


class Category(models.Model):
    name = models.CharField('Категория', max_length=225)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('home')


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(verbose_name='Изображения профиля', null=True, blank=True,
                                    upload_to='images/profile')
    website_url = models.URLField(max_length=255, null=True, blank=True)
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    instagram_url = models.URLField(max_length=255, null=True, blank=True)
    pinterest_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')


class Articles(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    header_image = models.ImageField(verbose_name='Изображения', null=True, blank=True, upload_to='images/')
    anons = models.CharField(verbose_name='Анонс', max_length=255)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    full_text = RichTextField(verbose_name='Статья', blank=True, null=True)
    post_date = models.DateTimeField(verbose_name='Дата публикации', default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):

        super(Articles, self).save(*args, **kwargs)

        if not self.header_image or int(self.header_image.height+(self.header_image.height/3)) == int(self.header_image.width):
            return

        img = Image.open(self.header_image.path)
        imgresize = img.resize((int(img.height+(img.height/3)), img.height), Image.ANTIALIAS)
        imgresize.save(self.header_image.path)

    def __str__(self):
        return f'Новость: {self.title}" | "{str(self.author)}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Comment(models.Model):
    post = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.post.title} - {self.name}'
