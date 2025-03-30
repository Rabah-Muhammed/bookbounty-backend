from django.urls import path
from .views import ( AddBookToReadingList, AllBooksView, BookDeleteView, BookDetailView,
                    BookListCreateView,BookUpdateView, ProfileView, ReadingListDetailView,
                    ReadingListView, RegisterView, LoginView,RemoveBookFromReadingListView, ReorderReadingListBooks)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:book_id>/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:book_id>/delete/", BookDeleteView.as_view(), name="book-delete"),
    path("all-books/", AllBooksView.as_view(), name="all-books"),
    path("books/<int:book_id>/detail/", BookDetailView.as_view(), name="book-detail"),
    path("reading-lists/", ReadingListView.as_view(), name="reading-list"),
    path("reading-lists/<int:pk>/", ReadingListDetailView.as_view(), name="reading-list-detail"),
    path("reading-lists/<int:list_id>/add-book/", AddBookToReadingList.as_view(), name="add-book"),
    path("reading-lists/<int:list_id>/remove/<int:book_id>/", RemoveBookFromReadingListView.as_view(), name="remove-book"),
    path('reading-lists/<int:list_id>/reorder/', ReorderReadingListBooks.as_view(), name='reorder-reading-list-books'),

]
