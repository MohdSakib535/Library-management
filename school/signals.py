from .models import MyUser,Books,Book_unique_no
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=Books)
def post_save_generator(sender,instance,created,*args,**kwargs):
    if created:
        Book_unique_no.objects.create(book_name=instance)