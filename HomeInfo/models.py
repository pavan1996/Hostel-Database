from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Person(models.Model):
	person_id 			= models.CharField(max_length=6, primary_key=True)
	registration_date 	= models.DateField(null=True)
	person_type 		= models.CharField(max_length=15,null=True)
	prefix 				= models.CharField(max_length=10,null=True)
	first_name 			= models.CharField(max_length=30,null=True)
	middle_name 		= models.CharField(max_length=30,null=True)
	last_name 			= models.CharField(max_length=30,null=True)
	house_number 		= models.CharField(max_length=10,null=True)
	house_name 			= models.CharField(max_length=30,null=True)
	land_mark 			= models.CharField(max_length=50,null=True)
	street_address 		= models.CharField(max_length=100,null=True)
	city 				= models.CharField(max_length=20,null=True) 
	state 				= models.CharField(max_length=20,null=True) 
	zipcode 			= models.CharField(max_length=6,null=True) 
	country 			= models.CharField(max_length=20,null=True) 
	date_of_birth 		= models.DateField(null=True)
	date_of_death 		= models.DateField(null=True)
	donation_frequency	= models.CharField(max_length=15,null=True)
	current_status 		= models.CharField(max_length=10,null=True)
	mode_of_communication = models.CharField(max_length=10,null=True)
	payment_mode 		= models.CharField(max_length=10,null=True)
	remarks 			= models.CharField(max_length=1000,null=True)
	period_of_stay_start= models.IntegerField(null=True)
	period_of_stay_end  = models.IntegerField(null=True)
	reference_person    = models.CharField(max_length=5, null=True)

	@property
	def fullname(self):
		return self.first_name + self.middle_name + self.last_name

class Phone(models.Model):
	person_id			= models.ForeignKey(Person, on_delete=models.CASCADE)
	phone_number		= models.CharField(null=True, max_length=10)

class Landline(models.Model):
	person_id			= models.ForeignKey(Person, on_delete=models.CASCADE)
	landline_number		= models.CharField(null=True, max_length= 10)


class Email(models.Model):
	person_id			= models.ForeignKey(Person, on_delete=models.CASCADE)
	email_address		= models.CharField(max_length=40,null=True) 

class PaymentMode(models.Model):
	payment_mode_id		= models.CharField(max_length=5, primary_key=True)
	payment_mode_desc	= models.CharField(max_length=100,null=True)
	payment_mode_remarks= models.CharField(max_length=100,null=True)

class Purpose(models.Model):
	purpose_id 			= models.CharField(max_length=5, primary_key=True)
	purpose_desc		= models.CharField(max_length=100, null=True )
	donation_type		= models.CharField(max_length=10, null=True)
	purpose_remarks     = models.CharField(max_length=100, null=True)

class Transaction(models.Model):
	receipt_date        = models.DateField(null=True)
	receipt_number		= models.CharField(max_length=5,null=True)
	person_id			= models.ForeignKey(Person, on_delete=models.CASCADE)
	payment_mode_id		= models.ForeignKey(PaymentMode, on_delete=models.CASCADE)
	donation_purpose_id = models.ForeignKey(Purpose, on_delete=models.CASCADE)
	payment_reference	= models.CharField(max_length=50,null=True)
	donation_amount		= models.IntegerField(null=True)
	donation_things     = models.CharField(max_length=100, null=True)
	transaction_remarks = models.CharField(max_length=100, null=True)