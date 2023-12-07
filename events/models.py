from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
# import pandas as pd
from events.utils import generate_ticket
from django.utils import timezone

def sheet_rename(instance, filename):
    ext = os.path.splitext(filename)[-1]
    new_filename = "uploads/event_%s/sheet%s" % (
        instance.slug, ext)

    return new_filename

def ticket_featured_photo_rename(instance, filename):
    ext = os.path.splitext(filename)[-1]
    new_filename = "uploads/event_%s/ticket_featured_photo%s" % (
        instance.slug, ext)

    return new_filename

def e_ticket_rename(instance, filename):
    ext = os.path.splitext(filename)[-1]
    new_filename = "uploads/event_%s/e_tickets/e_ticket_%s%s" % (
        instance.event.id,
        instance.slug, ext)

    return new_filename

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=255)
    location = models.CharField(max_length=755)
    venue = models.CharField(max_length=755)
    sheet = models.FileField(upload_to=sheet_rename)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_featured_photo = models.ImageField(upload_to=ticket_featured_photo_rename)


class UserRecord(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    sno = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    encoded_bar_code = models.CharField(max_length=255, null=True, blank=True)
    event_attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    e_ticket = models.ImageField(upload_to=e_ticket_rename, null=True, blank=True)

    def __str__(self):
        return f"{self.event.event_name}   |   {self.name}  -  {self.phone_number}"

# @receiver(post_save, sender=Event)
# def generateUserRecord(sender, instance, created, **kwargs):
#     try: 
# #        # if created:
#             excel_file_path = instance.sheet

#             df = pd.read_excel(excel_file_path, sheet_name='Main')

#             snos = df['sno'].tolist()
#             emails = df['email'].tolist()
#             names = df['name'].tolist()
#             numbers = df['number'].tolist()
#             is_create_records = df['add'].tolist()
#             #  = df['Create'].tolist()

            
#             # Create a list of YourModel instances
#             instances_to_create = []
#             for sno, email, name, number, is_create_record in zip(snos, emails, names, numbers,    is_create_records):
#                 if (is_create_record == 'no'):
#                     continue

#                 else:
#                     created_at = timezone.now()

#                     instances_to_create.append(UserRecord(event=Event.objects.get(id=instance.id), sno=sno, email=email, name=name, phone_number=number, created_at=created_at))

#             UserRecord.objects.bulk_create(instances_to_create)

#             for instance in instances_to_create:
#                 instance.refresh_from_db()
    
#     except Exception as e:
#         print(e)


# post_save.connect(generateUserRecord, sender=Event)