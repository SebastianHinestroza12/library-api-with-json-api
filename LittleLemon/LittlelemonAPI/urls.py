from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BooksView

router = DefaultRouter()
router.register(r'books', BooksView, basename='book')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
