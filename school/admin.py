from django.contrib import admin
from .models import MyUser,Books,Book_unique_no,Issue_book,Category,Favourite

# Register your models here.
admin.site.register(MyUser)


class BookAdmin(admin.ModelAdmin):
    list_display=['name','Author','category','created_at']
admin.site.register(Books,BookAdmin)


class Book_unique_no_Admin(admin.ModelAdmin):
    list_display=['id','book_name','icsb_no','created_at']
admin.site.register(Book_unique_no,Book_unique_no_Admin)

admin.site.register(Issue_book)
admin.site.register(Category)
admin.site.register(Favourite)
