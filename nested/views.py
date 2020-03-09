# Create your views here.
from rest_framework import viewsets

from nested.models import *
from nested_serializer_test.serializers import AppBaseSerializer


class ConceptSerializer(AppBaseSerializer):
    class Meta:
        model = Concept
        fields = '__all__'
        read_only_fields = ['chapter']


class PublisherSerializer(AppBaseSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class ChapterSerializer(AppBaseSerializer):
    concept = ConceptSerializer(many=True)

    class Meta:
        model = Chapter
        fields = '__all__'
        read_only_fields = ['author']

    def create(self, validated_data):
        concept = validated_data.pop("concept")
        instance = super().create(validated_data)
        self.nested_create(ConceptSerializer, concept, chapter=instance)
        return instance


class AuthorSerializer(AppBaseSerializer):
    chapter = ChapterSerializer(many=True)

    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ['book']

    def create(self, validated_data):
        chapter = validated_data.pop("chapter")
        instance = super().create(validated_data)
        self.nested_create(ChapterSerializer, chapter, author=instance)
        return instance


class BookSerializer(AppBaseSerializer):
    author = AuthorSerializer(many=True)
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        author = validated_data.pop("author")
        publisher = validated_data.pop("publisher")
        pub = self.nested_create(PublisherSerializer, publisher)
        validated_data['publisher'] = pub
        instance: Book = super(BookSerializer, self).create(validated_data)
        self.nested_create(AuthorSerializer, author, book=instance)
        return instance


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
