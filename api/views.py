from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics
from django.contrib.auth import get_user_model
from .models import Book, ReadingList, ReadingListBook
from .serializers import BookSerializer, CustomTokenObtainPairSerializer, ProfileSerializer, ReadingListSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction


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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.filter(created_by=request.user).order_by("-created_at")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
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
    permission_classes = [AllowAny]

    def get(self, request):
        books = Book.objects.all().order_by("-created_at")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class ReadingListView(generics.ListCreateAPIView):
    serializer_class = ReadingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReadingListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReadingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)


class AddBookToReadingList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, list_id):
        book_id = request.data.get("book_id")  
        if not book_id:
            return Response({"detail": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reading_list = ReadingList.objects.get(id=list_id, user=request.user)
            book = Book.objects.get(id=book_id)

            if ReadingListBook.objects.filter(reading_list=reading_list, book=book).exists():
                return Response({"detail": "Book already in reading list"}, status=status.HTTP_400_BAD_REQUEST)

            order = ReadingListBook.objects.filter(reading_list=reading_list).count()
            ReadingListBook.objects.create(reading_list=reading_list, book=book, order=order)

            return Response({"detail": "Book added to reading list"}, status=status.HTTP_201_CREATED)
        except ReadingList.DoesNotExist:
            return Response({"detail": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)


class RemoveBookFromReadingListView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, list_id, book_id):
        try:
            reading_list = ReadingList.objects.get(id=list_id, user=request.user)
            reading_list_book = ReadingListBook.objects.get(reading_list=reading_list, book__id=book_id)
            reading_list_book.delete()
            return Response({"detail": "Book removed from reading list"}, status=status.HTTP_200_OK)
        except ReadingList.DoesNotExist:
            return Response({"detail": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)
        except ReadingListBook.DoesNotExist:
            return Response({"detail": "Book not found in list"}, status=status.HTTP_404_NOT_FOUND)
        
        
class ReorderReadingListBooks(APIView):
    def put(self, request, list_id):
        try:
            reading_list = ReadingList.objects.get(id=list_id)
            books_data = request.data.get('books', [])
            
            with transaction.atomic():
                for book_data in books_data:
                    reading_list_book = ReadingListBook.objects.get(
                        id=book_data['id'],
                        reading_list=reading_list
                    )
                    reading_list_book.order = book_data['order']
                    reading_list_book.save()
            
            return Response(status=status.HTTP_200_OK)
        
        except ReadingList.DoesNotExist:
            return Response(
                {'detail': 'Reading list not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ReadingListBook.DoesNotExist:
            return Response(
                {'detail': 'Book not found in reading list'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )