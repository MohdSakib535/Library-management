from .models import MyUser,Category,Books,Book_unique_no,Issue_book,Favourite
from rest_framework import serializers


class User_data_serializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields='__all__'




class Category_data_serializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'


class Books_data_serializer(serializers.ModelSerializer):
    # category=Category_data_serializer(read_only=True)
    # or
    # category = serializers.CharField(source='category.type')
    class Meta:
        model=Books
        fields='__all__'
        # fields=['id','name','Author','category','book_img']


class book_unique_data_serializer(serializers.ModelSerializer):
    # book_name=Books_data_serializer()
    class Meta:
        model=Book_unique_no
        fields='__all__'


class Issue_book_data_serializer(serializers.ModelSerializer):
    # book_info=book_unique_data_serializer()
    # user=User_data_serializer()
    class Meta:
        model=Issue_book
        fields='__all__'
        # fields=['id','issue_date','return_date','book_info','user','status']




    