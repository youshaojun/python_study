from django.urls import path
from book.views import books, save, update, delete

urlpatterns = [
    path('hot', books),
    path('save', save),
    path('update/<book_id>', update),
    path('delete/<book_id>', delete),
]
