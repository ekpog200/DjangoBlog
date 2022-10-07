from django.db import models
from django.urls import reverse
from django.db import transaction
from django.template.defaultfilters import slugify


class Category (models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тэг')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class UserPlatformStats(models.Model):
    win = models.IntegerField(default=0,verbose_name='Пользователи Windows')
    mac = models.IntegerField(default=0, verbose_name='Пользователи Windows')
    iphone = models.IntegerField(default=0, verbose_name='Пользователи Windows')
    android = models.IntegerField(default=0, verbose_name='Пользователи Windows')
    other = models.IntegerField(default=0, verbose_name='Пользователи Windows')
    class Meta:
        verbose_name_plural = 'СтатистикаПО'

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название новости')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    author = models.CharField(max_length=255, verbose_name='Автор')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateField(auto_now_add=True, verbose_name='Время создания')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    news_day = models.BooleanField(verbose_name = 'Новость дня', default=False)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True,verbose_name = 'Тэги постов',)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.news_day:
            Post.objects.filter(
                news_day=True).update(news_day=False)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})
# Create your models here.
