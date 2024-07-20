from unicodedata import category
from django.shortcuts import render,redirect
from .models import Book_unique_no, MyUser,Books,Issue_book,Category,Favourite
from django.contrib.auth import authenticate,login as dj_login,logout 
from django.http import HttpResponseRedirect,HttpResponse
from itertools import chain
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def Home(request):
    id=request.user.id
    # print(id)
    return render(request,'home.html')
    
def login(request):
    if request.method=="POST":
        name=request.POST['name']
        password=request.POST['password']
        user=authenticate(username=name,password=password)
        print('user----',user)
        if user:
            dj_login(request,user)
            return redirect('h')
        else:
            return redirect('h')
    return render(request,'login.html')

def signup(request):
    if request.method=="POST":
        name=request.POST['name']
        designation=request.POST.get('dropdown',False)
        print('desigantion-----',designation)
        password=request.POST['password']

        newuser=MyUser.objects.create_user(username=name,designation=designation,password=password)
        newuser.save()
        return redirect('login')
    return render(request,'signup.html')
                

def Logout(request):
    logout(request)
    return redirect('h')


def Dashboard(request):
    user=request.user
    return render(request,'dashboard.html')


def Add_books(request):
    category_books=Category.get_all_categories()
    if request.method=="POST":
        name=request.POST['name']
        author=request.POST['author']
        category=request.POST.get('category',None)
        c=Category.objects.get(id=category)
        image_book=request.FILES.get('image_book',None)
        add_book_data=Books.objects.create(name=name,Author=author,category=c,book_img=image_book)
        add_book_data.save()
        return redirect('add_books')

    return render(request,'add_books.html',context={'category':category_books})

@login_required(login_url='h')
def All_books(request):
    book_no=Book_unique_no.objects.all()
    category=Category.objects.all()

    return render(request,'all_books.html',context={'books':book_no,'category':category})


def Edit_books(request,id):
    print('id---',id)
    if request.method =="POST":
        name=request.POST['name']
        author=request.POST['author']
        category=request.POST['category']
        print('category-------',category)
        c1=Category.objects.get(id=category)
        Books.objects.filter(id=id).update(name=name,Author=author,category=c1)
        return redirect('all_books')


def Update_books(request):
    return redirect('all_books')

def Delete(request,id):
    delete_data=Books.objects.get(id=id)
    delete_data.delete()
    return redirect('all_books')

def Profile(request):
    m=''
    user_id=MyUser.objects.filter(id=request.user.id)
    data=request.user
    issue_book_data=Issue_book.objects.all()
    for m in issue_book_data:
        pass

    if request.method=="POST":
            data.username = request.POST.get('name',None)
            data.designation = request.POST['designation']
            data.save()
            return redirect('profile')
    return render(request,'profile.html',context={'a':user_id,'issue_book_data':issue_book_data,'m':m})

def Delete_user(request,id):
    delete_user=MyUser.objects.get(id=id)
    delete_user.delete()
    return redirect('profile')




def Available_books(request):
    # available_books=Book_unique_no.objects.all() 
    available_categories=Category.get_all_categories()
    category_id = request.GET.get('category')

    
    if category_id is not None :
        available_books=Books.objects.filter(category=category_id )
      
        d2=[]
        for i in available_books:
            d2.append(Book_unique_no.objects.get(id=i.id))
       
    else:
        available_books=Books.objects.all() 
        
        d2=[]
        for i in available_books:
           d2.append(Book_unique_no.objects.get(id=i.id))

        a=Issue_book.objects.all()
        for i in a:
            pass
            
    return render(request,'all_available_books.html',context={'data':zip(available_books,tuple(d2)),'available_categories':available_categories,})


def Favourite_Book(request):
    user=request.user
    print('user------',user)
    unique_book_id=request.GET.get('unique_id')
    
    unique_book_id_data=Book_unique_no.objects.filter(id=unique_book_id)
   
    for i in unique_book_id_data:
        if not Favourite.objects.filter(unique_id=i,user_data=user).exists():
          fav=Favourite.objects.create(unique_id=i,user_data=user)
          fav.save()
        else:
            messages.add_message(request, messages.WARNING, 'Already exist')
    return redirect('available_books')

def Book_details(request,id):
    detail_book=Book_unique_no.objects.get(id=id)
    return render(request,'book_detail.html',{'book_detail':detail_book})


def My_Books(request):
    fav_book_id=request.GET.get('unique_id')
    
    if fav_book_id:
        b=Favourite.objects.get(id=fav_book_id)
        b.delete()
        return redirect('mybook')
    else:
        user=request.user
        print('user-----',user)
        book_collections=Favourite.objects.filter(user_data=user).all()
        


    return render(request,'mybooks.html',context={'m':book_collections})



def All_User(request):
    all_user=MyUser.objects.exclude(is_superuser=True).all()
    return render(request,'all_user.html',{'all_user':all_user,})

def Delete_User_by_admin(request,id):
    delete_user=MyUser.objects.get(id=id)
    # issued_book = len(Issue_book.objects.filter(user=MyUser).all())
    # if issued_book == 0:
    #     delete_user.delete()
    # else:
    #     pass
    delete_user.delete()
    return redirect('all_user')

def Issue_Detail(request,id):
    if request.user.is_authenticated:
        user=request.user
        book_name=Book_unique_no.objects.filter(id=id)
        
        for i in book_name:
            book_id=i
            # print('i-----',i)
        issue_data=''
        
        if request.method == "POST":
            issue_date=request.POST['issue_date']
            return_date=request.POST['return_date']
            book_name_status=request.POST['book_name_status']
            issue_data=Issue_book.objects.create(issue_date=issue_date,return_date=return_date,book_info=book_id,user=user,status=book_name_status)
            issue_data.save()
            Books.objects.filter(id=i.id).update(status=book_name_status)
        return redirect('available_books')
    else:
        return HttpResponseRedirect('/')


def Book_issue(request):
    user=request.user
    if user.is_superuser==True:
        book_issue=Issue_book.objects.all()
        l=[]
        for i in book_issue:
            t=date.today()

            if t > i.return_date:
                a=abs(t-i.return_date).days
                fine= int(a*5)
                l.append(fine)
            elif(t<i.return_date or t==i.return_date):
               fine=0
               l.append(fine)
    else:
        book_issue=Issue_book.objects.filter(user=user).all()
        l=[]
        for i in book_issue:
            t=date.today()
            if t > i.return_date:
                a=abs(t-i.return_date).days
                fine= int(a*5)
                l.append(fine)
            elif(t<i.return_date or t==i.return_date):
               fine=0
               l.append(fine)
    return render(request,'book_issue.html',context={'book_issue':zip(book_issue,l)})


def Return_Book(request,id,):
    q=Issue_book.objects.filter(id=id)
    for i in q:
        pass
    if request.method == 'POST':
        book_name_status=request.POST['book_name_status']
        Books.objects.filter(id=i.book_info.id).update(status=book_name_status)
    q.delete()
    return redirect('book_issue')



# api data

from rest_framework.views import APIView
from .serializer import Category_data_serializer,User_data_serializer,Books_data_serializer,book_unique_data_serializer,Issue_book_data_serializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework import filters

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from django_filters import  rest_framework as filter
from django_filters.rest_framework import DjangoFilterBackend


class MyModelFilter(filter.FilterSet):
    name = filter.CharFilter(field_name='username', lookup_expr='icontains')
    class Meta:
        model =MyUser
        fields = ['name']


# class User_Data(viewsets.ModelViewSet):
#     queryset=MyUser.objects.all()
#     serializer_class=User_data_serializer
#     authentication_classes=[SessionAuthentication]
#     # permission_classes=[IsAuthenticatedOrReadOnly]
#     permission_classes=[IsAuthenticated]
#     throttle_classes=[UserRateThrottle]
#     filter_backends = [filters.OrderingFilter,DjangoFilterBackend]
#     filter_class = MyModelFilter
#     ordering_fields = ['created_at']


class User_Data(viewsets.ModelViewSet):
    queryset=MyUser.objects.all()
    serializer_class=User_data_serializer
    authentication_classes=[SessionAuthentication]
    # authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    # throttle_classes=[UserRateThrottle]
    # filter_backends = [filters.OrderingFilter,DjangoFilterBackend]
    # filter_class = MyModelFilter
    # ordering_fields = ['created_at']




class Category_Data(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get(self,request,id=None):
        if id is not None:
            category_data=Category.objects.get(id=id)
            serializer=Category_data_serializer(category_data)
            return Response(serializer.data)
        category_data=Category.objects.all()
        serializer=Category_data_serializer(category_data,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=Category_data_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'user data created successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_406_NOT_ACCEPTABLE)


# class Books_Data(APIView):
#     def get(self,request,pk=None):
#         print('pk------',pk)
#         if pk is not None:
#             try:
#                 books_data=Books.objects.get(pk=pk)
#                 serializer=Books_data_serializer(books_data)
#                 return Response(serializer.data)
#             except Books.DoesNotExist:
#                 raise HttpResponse(status=status.HTTP_404_NOT_FOUND)
#         books_data=Books.objects.all()
#         serializer=Books_data_serializer(books_data,many=True)
#         return Response(serializer.data)
    
#     def post(self,request,format=None):
#         serializer=Books_data_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'user data created successfully'},status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
#     def put(self,request,pk=None):
#         books_data=Books.objects.get(pk=pk)
#         serializer=Books_data_serializer(books_data,request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({'msg':'update successfully'})
#         return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)
    
#     def patch(self,request,pk=None):
#         books_data=Books.objects.get(pk=pk)
#         serializer=Books_data_serializer(books_data,request.data,partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({'msg':'partiall update successfully'})
#         return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)
    

#     def delete(self,request,pk=None,format=None):
#         stu=Books.objects.get(id=pk)
#         stu.delete()
#         return Response({'msg':'deleted Data'})
    
class Book_Data(viewsets.ModelViewSet):
    queryset=Books.objects.all()
    serializer_class=Books_data_serializer
    permission_classes=[IsAuthenticatedOrReadOnly]
  


class Book_unique_Data(viewsets.ModelViewSet):
    queryset=Book_unique_no.objects.all()
    serializer_class=book_unique_data_serializer
    permission_classes=[IsAuthenticatedOrReadOnly]


class Issue_book_Data(viewsets.ModelViewSet):
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]
    queryset=Issue_book.objects.all()
    serializer_class=Issue_book_data_serializer




            





