import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator

from rest_framework import viewsets, filters as rest_framework_filters
from rest_framework.response import Response
from rest_framework_json_api import django_filters, filters
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from .serializers import BookSerializer
from .models import Book
from rest_framework.decorators import action

class BooksView(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_deleted=False)
    serializer_class = BookSerializer
    filter_backends = [
        filters.QueryParameterValidationFilter, filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
        rest_framework_filters.SearchFilter
    ]
    filterset_fields = {
        'id': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
        'price': ('exact', 'lt', 'gt', 'gte', 'lte'),
        'inventory': ('exact', 'lt', 'gt', 'gte', 'lte'),
        'created_at': ('exact', 'lt', 'gt', 'gte', 'lte'),
        'updated_at': ('exact', 'lt', 'gt', 'gte', 'lte'),
        'author': ('icontains', 'iexact', 'contains', 'exact'),
        'title': ('icontains', 'iexact', 'contains', 'exact'),
    }
    search_fields = ('author', 'title')
    ordering_fields = ('author', 'title', 'price', 'inventory', 'created_at', 'updated_at')

    def create(self, request, *args, **kwargs):
        data = request.data
        book = Book.create_book(data)
        serializer = self.get_serializer(book)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        book = Book.get_book_by_id(pk)
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    def update(self, request, pk=None):
        data = request.data
        book = Book.objects.filter(pk=pk, is_deleted=False).first()
        if book:
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            book.price = data.get('price', book.price)
            book.inventory = data.get('inventory', book.inventory)
            book.save()
            serializer = self.get_serializer(book)
            return Response(serializer.data)
        raise NotFound(detail="Resource not found")

    def destroy(self, request, pk=None):
        book = Book.delete_book(pk)
        if book:
            return Response(status=HTTP_204_NO_CONTENT)
        raise NotFound(detail="Resource not found")

    @action(detail=True, methods=['patch'], url_path='restore')
    def restore(self, request, pk=None):
        book = Book.restore_book(pk)
        if book:
            return Response(status=HTTP_204_NO_CONTENT)
        raise NotFound(detail="Resource not found")

    @action(detail=True, methods=['delete'], url_path='force-delete')
    def force_delete(self, request, pk=None):
        book = Book.force_delete_book(pk)
        if book:
            return Response(status=HTTP_204_NO_CONTENT)
        raise NotFound(detail="Resource not found")
