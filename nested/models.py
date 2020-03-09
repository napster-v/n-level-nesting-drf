from django.db import models


# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True)


class Author(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='author')
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)


class Chapter(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='chapter')
    number = models.IntegerField()


class Concept(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='concept')
    topic = models.CharField(max_length=100)
