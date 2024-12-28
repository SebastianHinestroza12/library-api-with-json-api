from django.db import models

class BookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=250)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    inventory = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #objects = BookManager()

    @classmethod
    def get_all_books(cls):
        return cls.objects.filter(is_deleted=False)

    @classmethod
    def create_book(cls, data):
        book = cls(
            title=data.get('title'),
            author=data.get('author'),
            price=data.get('price'),
            inventory=data.get('inventory')
        )
        book.save()
        return book

    @classmethod
    def get_book_by_id(cls, bookId):
        return cls.objects.filter(pk=bookId, is_deleted=False).first()

    @classmethod
    def delete_book(cls, bookId):
        book = cls.objects.filter(pk=bookId, is_deleted=False).first()
        if book:
            book.is_deleted = True
            book.save()
        return book

    @classmethod
    def force_delete_book(cls, bookId):
        book = cls.objects.filter(pk=bookId, is_deleted=True).first()
        if book:
            book.delete()
        return book

    @classmethod
    def restore_book(cls, bookId):
        book = cls.objects.filter(pk=bookId, is_deleted=True).first()
        print(book)
        if book:
            book.is_deleted = False
            book.save()
        return book

    class JSONAPIMeta:
        resource_name = "books"
