from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Inquiry(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 254)
    phone_no = PhoneNumberField(null=False, blank=False, unique=False)
    product_start_date =  models.DateField()
    product_end_date =  models.DateField()
    complain_message = models.TextField()

    # def __str__(self):
    #     return self.customer_name, self.email
