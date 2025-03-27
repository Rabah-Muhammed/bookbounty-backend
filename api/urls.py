from django.urls import path
from .views import AllBooksView, BookDeleteView, BookDetailView, BookListCreateView, BookUpdateView, ProfileView, RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("books/", BookListCreateView.as_view(), name="book-list-create"),  # User's books
    path("books/<int:book_id>/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:book_id>/delete/", BookDeleteView.as_view(), name="book-delete"),
    path("all-books/", AllBooksView.as_view(), name="all-books"),
    path("books/<int:book_id>/detail/", BookDetailView.as_view(), name="book-detail"),

]
