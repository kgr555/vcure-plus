from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.urls import reverse
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.cache import cache 
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
from django.db.models import Sum
from django.conf import settings

import datetime
from decimal import Decimal


class CustomUser(AbstractUser):
    user_type_data = ((1, "AdminHOD"), (2, "Pharmacist"), (3, "Doctor"), (4, "PharmacyClerk"),(5, "Patients"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class Patients(models.Model):
    gender_category=(
        ('Male','Male'),
        ('Female','Female'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    reg_no=models.CharField(max_length=30,null=True,blank=True,unique=True)
    gender=models.CharField(max_length=7,null=True,blank=True,choices=gender_category)
    first_name=models.CharField(max_length=20,null=True,blank=True)
    last_name=models.CharField(max_length=20,null=True,blank=True)
    dob=models.DateTimeField(auto_now_add= False, auto_now=False,null=True,blank=True)
    phone_number=models.CharField(max_length=10,null=True,blank=True)
    profile_pic=models.ImageField(default="patient.jpg",null=True,blank=True)
    age= models.IntegerField(default='0', blank=True, null=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    date_admitted=models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.admin)



class AdminHOD(models.Model):
    gender_category=(
        ('Male','Male'),
        ('Female','Female'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    emp_no= models.CharField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,choices=gender_category)
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="admin.png",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_employed=models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)
    


class Pharmacist(models.Model):
    gender_category=(
        ('Male','Male'),
        ('Female','Female'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    emp_no=models.CharField(max_length=100,null=True,blank=True)
    age= models.IntegerField(default='0', blank=True, null=True)
    gender=models.CharField(max_length=100,null=True,choices=gender_category)
    mobile =models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="images2.png",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)

    
class Doctor(models.Model):
    gender_category=(
        ('Male','Male'),
        ('Female','Female'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    emp_no=models.CharField(max_length=100,null=True,blank=True)
    age= models.IntegerField(default='0', blank=True, null=True)
    gender=models.CharField(max_length=100,null=True,choices=gender_category)
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="doctor.png",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)
	

class PharmacyClerk(models.Model):
    gender_category=(
        ('Male','Male'),
        ('Female','Female'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    emp_no=models.CharField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,choices=gender_category)
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="images2.png",null=True,blank=True)
    age= models.IntegerField(default='0', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)
	
    

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    
    def __str__(self):
        return str(self.name)
	

    
class Prescription(models.Model):
    patient_id = models.ForeignKey(Patients,null=True, on_delete=models.SET_NULL)
    description=models.TextField(null=True)
    prescribe=models.CharField(max_length=100,null=True)
    date_precribed=models.DateTimeField(auto_now_add=True, auto_now=False)




class ExpiredManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
        )

class Stock(models.Model):
    category = models.ForeignKey(Category,null=True,on_delete=models.CASCADE,blank=True)
    drug_imprint=models.CharField(max_length=6 ,blank=True, null=True)
    drug_name = models.CharField(max_length=50, blank=True, null=True)
    drug_color = models.CharField(max_length=50, blank=True, null=True)
    drug_shape = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    manufacture= models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    drug_strength= models.CharField(max_length=10, blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True,default=timezone.now)
    valid_to = models.DateTimeField(blank=False, null=True)
    drug_description=models.TextField(blank=True,max_length=1000,null=True)
    drug_pic=models.ImageField(default="images2.png",null=True,blank=True)
    unit_price= models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    objects = ExpiredManager()
   
    def __str__(self):
        return str(self.drug_name)
   
    
class Dispense(models.Model):
    
    patient_id = models.ForeignKey(Patients, on_delete=models.DO_NOTHING,null=True)
    drug_id = models.ForeignKey(Stock, on_delete=models.SET_NULL,null=True,blank=False)
    dispense_quantity = models.PositiveIntegerField(default='1', blank=False, null=True)
    taken=models.CharField(max_length=300,null=True, blank=True)
    stock_ref_no=models.CharField(max_length=300,null=True, blank=True)
    instructions=models.TextField(max_length=300,null=True, blank=False)
    dispense_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)


class PatientFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    admin_id= models.ForeignKey( AdminHOD,null=True, on_delete=models.CASCADE)
    pharmacist_id=models.ForeignKey( Pharmacist,null=True, on_delete=models.CASCADE)
    feedback = models.TextField(null=True)
    feedback_reply = models.TextField(null=True)
    admin_created_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Order(models.Model):    
    title = models.CharField(blank=True, max_length=150)
    patient_id = models.ForeignKey(Patients, on_delete=models.DO_NOTHING,null=True)
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    ordered_at = models.DateField(default=datetime.datetime.now())
    ordered = models.BooleanField(default=False)
    # class Meta:
    #     ordering = ['-date']

    # def save(self, *args, **kwargs):
    #     order_items = self.order_items.all()
    #     self.value = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
    #     self.final_value = Decimal(self.value) - Decimal(self.discount)
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return f'{self.patient_id.first_name}'

    # def get_edit_url(self):
    #     return reverse('update_order', kwargs={'pk': self.id})

    # def get_delete_url(self):
    #     return reverse('delete_order', kwargs={'pk': self.id})

    # def tag_final_value(self):
    #     return f'{self.final_value} {CURRENCY}'

    # def tag_discount(self):
    #     return f'{self.discount} {CURRENCY}'

    # def tag_value(self):
    #     return f'{self.value} {CURRENCY}'

    # @staticmethod
    # def filter_data(request, queryset):
    #     search_name = request.GET.get('search_name', None)
    #     date_start = request.GET.get('date_start', None)
    #     date_end = request.GET.get('date_end', None)
    #     queryset = queryset.filter(title__contains=search_name) if search_name else queryset
    #     if date_end and date_start and date_end >= date_start:
    #         date_start = datetime.datetime.strptime(date_start, '%m/%d/%Y').strftime('%Y-%m-%d')
    #         date_end = datetime.datetime.strptime(date_end, '%m/%d/%Y').strftime('%Y-%m-%d')
    #         print(date_start, date_end)
    #         queryset = queryset.filter(date__range=[date_start, date_end])
    #     return queryset


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    drug_id = models.ForeignKey(Stock, on_delete=models.SET_NULL,null=True,blank=False)   
    quantity = models.PositiveIntegerField(default='1', blank=False, null=True)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

    # def __str__(self):
    #     return f'{self.drug_id.drug_name}'

    # def save(self,  *args, **kwargs):
    #     self.final_price = self.discount_price if self.discount_price > 0 else self.price
    #     self.total_price = Decimal(self.qty) * Decimal(self.final_price)
    #     super().save(*args, **kwargs)
    #     self.order.save()

    # def tag_final_price(self):
    #     return f'{self.final_price} {CURRENCY}'

    # def tag_discount(self):
    #     return f'{self.discount_price} {CURRENCY}'

    # def tag_price(self):
    #     return f'{self.price} {CURRENCY}'


# @receiver(post_save, sender=OrderItems)
# def correct_price(sender, **kwargs):
#     order_items = kwargs['instance']
#     price_of_product = Stock.objects.get(id=order_items.drug_id.id)
#     order_items.price = order_items.quantity * float(price_of_product.unit_price)
#     # total_cart_items = OrderItems.objects.filter(patient_id = order_items.patient_id)
#     # order_items.total_items = len(total_cart_items)
    
#     order = Order.objects.get(id = order_items.order.id)
#     order.total_price = order_items.price
#     order.save()



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Pharmacist.objects.create(admin=instance,address="")
        if instance.user_type == 3:
            Doctor.objects.create(admin=instance,address="")
        if instance.user_type == 4:
            PharmacyClerk.objects.create(admin=instance,address="")
        if instance.user_type == 5:
            Patients.objects.create(admin=instance,address="")
       
       
       

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.pharmacist.save()
    if instance.user_type == 3:
        instance.doctor.save()
    if instance.user_type == 4:
        instance.pharmacyclerk.save()
    if instance.user_type == 5:
        instance.patients.save()


   



 