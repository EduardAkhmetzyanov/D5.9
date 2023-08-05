from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)

    def update_rating(self):
        rank_posts_author = Post.objects.filter(author=self).aggregate(Sum('rank'))['rank__sum'] * 3
        rank_comment_author = Comment.objects.filter(user=self.user).aggregate(Sum('rank'))['rank__sum']
        rank_comment_posts_author = Comment.objects.filter(post__author__user = self.user).aggregate(Sum('rank'))['rank__sum']

        self.rank = rank_posts_author + rank_comment_author + rank_comment_posts_author
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True, verbose_name='Категория')


class Post(models.Model):
    article = 'AR'
    news = "NW"

    POST = [(article, "статья"),
            (news, 'новость')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.CharField(max_length=2, choices=POST, verbose_name='Вид поста')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    header = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(max_length=2048, verbose_name='Текст')
    category = models.ManyToManyField(Category, through='PostCategory')
    rank = models.IntegerField(default=0)

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        self.rank -= 1
        self.save()

    def prewiew(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.CharField(max_length=255, verbose_name='Комментарий')
    time_com = models.DateTimeField(auto_now_add=True, verbose_name='Время создания комментария')
    rank = models.IntegerField(default = 0)

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        self.rank -= 1
        self.save()

