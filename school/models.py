from random import choices
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
import random



class MyUserManager(BaseUserManager):
    def create_user(self,username, designation , password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            designation=designation,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,designation, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            designation=designation,
            password=password,
        )
        user.is_admin = True
        user.is_superuser=True
        user.save(using=self._db)
        return user

CHOICES =(
    ("Member", "Member"),
    ("Librarian", "Librarian"),
)

class MyUser(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=20,unique=True)
    designation=models.CharField(max_length=20,choices=CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['designation']

    def __str__(self):
        return str(self.id)
        # return self.username
        # return f"{self.username},{str(self.id)}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


BOOK_CHOICES = (
("fantasy","fantasy"),
("Science","Science"),
("Adventure","Adventure"),
("History","History"),
("learning","learning"),
)



class Category(models.Model):
    type=models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        # return self.type
        return f"{self.type},{str(self.id)}"

   
status_choice=(
    ('active','active'),
    ('borrow','borrow'),
)

class Books(models.Model):
    name=models.CharField(max_length=20)
    Author=models.CharField(max_length=20)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    book_img=models.ImageField(upload_to='book_image',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=status_choice,default='active',max_length=10)
    



    def __str__(self):
        # return str(self.id)
        return f"{str(self.id)},{self.name}"


class Book_unique_no(models.Model):
    book_name=models.OneToOneField(Books,on_delete=models.CASCADE,related_name='book_name')
    icsb_no=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.book_name)

    def save(self,*args,**kwargs):
        list=['a','b','c','d','e','f']
        number=[x for x in range(10)]
        list.extend(number)
        c=[]
        for i in range(7):
            num=random.choice(list)
            c.append(num)
        d="".join(str(j) for j in c)
        self.icsb_no=d
        super().save(*args,**kwargs)

# class  my_collections(models.model):
#     name=models.CharField(max_length=20,null=True,blank=True)


class Issue_book(models.Model):
    issue_date=models.DateField()
    return_date=models.DateField()
    book_info=models.ForeignKey(Book_unique_no,on_delete=models.CASCADE,related_name='book_info')
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='user_info')
    status=models.CharField(choices=status_choice,max_length=10)
    

class Favourite(models.Model):
    unique_id=models.ForeignKey(Book_unique_no,on_delete=models.CASCADE,related_name='unique_id')
    user_data=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='user_data')
    
    # def __str__(self):
    #     return self.id





