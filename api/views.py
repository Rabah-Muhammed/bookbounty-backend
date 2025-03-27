from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Book
from .serializers import BookSerializer, CustomTokenObtainPairSerializer, ProfileSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the authenticated user's profile"""
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        """Update the authenticated user's profile"""
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BookListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Require auth for listing user's books

    def get(self, request):
        """List books created by the authenticated user"""
        books = Book.objects.filter(created_by=request.user).order_by("-created_at")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new book"""
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.created_by != request.user:
                return Response({"detail": "You can only edit your own books"}, status=status.HTTP_403_FORBIDDEN)
            serializer = BookSerializer(book, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

class BookDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.created_by != request.user:
                return Response({"detail": "You can only delete your own books"}, status=status.HTTP_403_FORBIDDEN)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

class AllBooksView(APIView):
    permission_classes = [AllowAny]  # Public access to all books

    def get(self, request):
        """List all books from all users"""
        books = Book.objects.all().order_by("-created_at")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    
class BookDetailView(APIView):
    permission_classes = [AllowAny]  # Public access for details

    def get(self, request, book_id):
        """Retrieve a single book's details"""
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)