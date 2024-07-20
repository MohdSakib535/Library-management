"""librarymanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from school import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView

router=DefaultRouter()
router.register('user_data',views.User_Data)
router.register('Book_Data',views.Book_Data)
router.register('Book_unique_Data',views.Book_unique_Data)
router.register('Issue_book_Data',views.Issue_book_Data)






urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home,name='h'),
    path('login/',views.login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('d/',views.Dashboard,name='d'),
    path('ab/',views.Add_books,name='add_books'),
    path('aab/',views.All_books,name='all_books'),
    path('edit-books/<int:id>/',views.Edit_books,name='edit_book'),
    path('ub/',views.Update_books,name='update_books'),
    path('d/<int:id>',views.Delete,name='delete'),
    path('avb/',views.Available_books,name='available_books'),
    # path('avb<slug:slug>/',views.Available_books,name='available_books'),
    path('bd/<int:id>/',views.Book_details,name='book_detail'),
    path('mb/',views.My_Books,name='mybook'),
    path('au/',views.All_User,name='all_user'),
    path('du/<int:id>/',views.Delete_User_by_admin,name='delete_user_by_admin'),
    path('ib/<int:id>/',views.Issue_Detail,name='issue_book'),
    path('bi/',views.Book_issue,name='book_issue'),
    path('rb/<int:id>/',views.Return_Book,name='return_book'),
    path('p/',views.Profile,name='profile'),
    path('delete_user/<int:id>/',views.Delete_user,name='delete_user'),
    # path('edit/',views.Edit,name='edit'),
    path('fav/',views.Favourite_Book,name='favourite_book'),



    # api data
    path('api/',include(router.urls)),

    path('auth/',include('rest_framework.urls')),
    


    path('user',views.User_Data.as_view({'get': 'list','post':'create'})),
    path('user/<int:pk>',views.User_Data.as_view({'get': 'retrieve','put':'update','patch':'partial_update','delete':'destroy'})),
    path('c/',views.Category_Data.as_view()),
    path('c/<int:id>/',views.Category_Data.as_view()),
    # path('b/',views.Books_Data.as_view()),
    # path('b/<int:pk>/',views.Books_Data.as_view()),



 


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
   

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
