from __future__ import unicode_literals
from django.db import connection
from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .models import Person
from .filters import PersonFilter
import xlwt
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Value
from django.db.models.functions import Concat


def index(request):
	return render(request, 'HomeInfo/index.html')

def about(request):
	return render(request, 'HomeInfo/about.html')

def contact(request):
	return render(request, 'HomeInfo/contact.html')

def infoentry(request):
	if request.method == 'GET':
		return render(request, 'HomeInfo/form.html' )
	elif request.method == 'POST':
		postData = request.POST
		person = Person()
		cursor = connection.cursor()
		now = datetime.datetime.now()
		current_date =now.strftime("%Y-%m-%d")


		person.person_type 		= postData.get('q13_typeA')
		person.first_name 		= postData.get('q3_fullName3[first]')
		
		#for ID generetion
		name_first_leter        = person.first_name[0]
		print(name_first_leter)
		print(person.person_type)

		

		if person.person_type == "Home":
			cursor.execute("SELECT count(*) FROM HomeInfo_person WHERE left(first_name,1) = '%s' AND person_type = 'Home' " %name_first_leter)
			number_of_persons =cursor.fetchone()
			print(number_of_persons)
			ID = "H" + name_first_leter + str(number_of_persons[0]+1).zfill(3)

			

		elif person.person_type == "Trust":
			cursor.execute("SELECT count(*) FROM HomeInfo_person WHERE left(first_name,1) = '%s' AND person_type = 'Trust' " %name_first_leter)
			number_of_persons =cursor.fetchone()
			print(number_of_persons)
			ID = "T" + name_first_leter + str(number_of_persons[0]+1).zfill(3)

		elif person.person_type == "Miscellaneous":
			cursor.execute("SELECT count(*) FROM HomeInfo_person WHERE left(first_name,1) = '%s' AND person_type = 'Miscellaneous' " %name_first_leter)
			number_of_persons =cursor.fetchone()
			print(number_of_persons)
			ID = "D" + name_first_leter + str(number_of_persons[0]+1).zfill(3)
		else:
			print("Somthing is wrong")
			return render(request, 'HomeInfo/ErrorInSubmission.html')

		#for ID generetion END 
		person.prefix 			= postData.get('q3_fullName3[prefix]')  
		person.middle_name 		= postData.get('q3_fullName3[middle]')
		person.last_name 		= postData.get('q3_fullName3[last]')
		person.registration_date= current_date
		person.person_id 		= ID
		person.house_number 	= postData.get('q22_input22')
		person.house_name 		= postData.get('q23_input23')
		person.land_mark 		= postData.get('q21_address[addr_line1]')
		person.street_address 	= postData.get('q21_address[addr_line2]')
		person.city 			= postData.get('q21_address[city]')
		person.state 			= postData.get('q21_address[state]')
		person.zipcode 			= postData.get('q21_address[postal]')
		person.country 			= postData.get('q21_address[country]')

		date_of_birth_not_formated 	= postData.get('Date_of_Birth')
		print(date_of_birth_not_formated)
		if date_of_birth_not_formated != "":
			month,date,year 		= date_of_birth_not_formated.split('/')
			person.date_of_birth 	= str(year) + "-" + str(month) + "-" + str(date)

		date_of_death_not_formated 	= postData.get('Date_of_Death')
		if date_of_death_not_formated != "":
			month1,date1,year1 		= date_of_death_not_formated.split('/')
			person.date_of_death 	= str(year1) + "-" + str(month1) + "-" + str(date1)
		
		print person.date_of_death
		person.donation_frequency	= postData.get('q17_donationFrequency')
		person.current_status 	    = postData.get('q18_typeA18')
		person.mode_of_communication= postData.get('q19_typeA19')
		person.payment_mode 	    = postData.get('q26_typeA26')
		person.reference_person     = postData.get('reference_person')
		person.remarks              = postData.get('q12_suggestionsOr12')
		person.period_of_stay_start = postData.get('period_of_stay_start')
		person.period_of_stay_end   = postData.get('period_of_stay_end')
		person.save()

		number_of_phone 		= int(postData.get('number_of_phone')) + 1
		number_of_landline 		= int(postData.get('number_of_landline')) + 1
		number_of_email 		= int(postData.get('number_of_email')) + 1

		for i in range(1, number_of_phone ):
			phone   					= Phone()
			person_foreignkey_object 	= Person.objects.all().filter(person_id = ID)
			phone.person_id				= person_foreignkey_object[0]
			phone.phone_number  		= postData.get('phone[' + str(i) + '][number]') 
			phone.save()

		for i in range(1, number_of_landline):
			landline 					= Landline()
			person_foreignkey_object 	= Person.objects.all().filter(person_id = ID)
			landline.person_id			= person_foreignkey_object[0]
			landline.landline_number  	= postData.get('landline[' + str(i) + '][number]') 
			landline.save()

		for i in range(1, number_of_email):
			print("hello")
			email 	 					= Email()
			person_foreignkey_object 	= Person.objects.all().filter(person_id = ID)
			email.person_id				= person_foreignkey_object[0]
			email.email_address  		= postData.get('email[' + str(i) + '][number]') 
			email.save()

		for i in range(1, number_of_email):
			print("")
		
		print("person created with id "+person.person_id)
		person_info = {'name': person.prefix +" "+ person.first_name + " "+ person.middle_name + " "+ person.last_name, 'id':person.person_id }
		return render(request, 'HomeInfo/submitSuccess.html', person_info)
	   

def updateInfo(request, id):
	if request.method == 'GET':
		person_object 		= Person.objects.all().filter(person_id = id)

		date_of_birth_not_formated = person_object[0].date_of_birth
		if date_of_birth_not_formated:
			date_of_birth    			= date_of_birth_not_formated.strftime('%m/%d/%Y')
		else:
			date_of_birth 				= None
		

		date_of_death_not_formated = person_object[0].date_of_death
		if date_of_death_not_formated:
			date_of_death    			= date_of_death_not_formated.strftime('%m/%d/%Y')
		else:
			date_of_death     			= None
		phone_object 		= Phone.objects.all().filter(person_id = id)
		phone_list			= []
		for i in phone_object:
			phone_list.append(i.phone_number)

		landline_object 	= Landline.objects.all().filter(person_id = id)
		landline_list		= []
		for i in landline_object:
			landline_list.append(i.landline_number)

		email_object 		= Email.objects.all().filter(person_id = id)
		email_list			= []
		for i in email_object:
			email_list.append(i.email_address)


		
		person = {
			'person_type'			: person_object[0].person_type ,
			'prefix' 				: person_object[0].prefix ,
			'first_name' 			: person_object[0].first_name,
			'middle_name'			: person_object[0].middle_name,
			'last_name' 			: person_object[0].last_name,

			'date_of_birth'			: date_of_birth,
			'date_of_death'			: date_of_death,


			'house_number'			: person_object[0].house_number,
			'house_name'			: person_object[0].house_name,
			'land_mark' 			: person_object[0].land_mark,
			'street_address'		: person_object[0].street_address,
			'city'					: person_object[0].city,
			'state'					: person_object[0].state,
			'zipcode'    			: person_object[0].zipcode,
			'country' 				: person_object[0].country,
			'phone'					: phone_list,
			'landline'				: landline_list,
			'email'					: email_list,
			'donation_frequency'	: person_object[0].donation_frequency,
			'current_status'		: person_object[0].current_status,
			'payment_mode'			: person_object[0].payment_mode,
			'mode_of_communication' : person_object[0].mode_of_communication,
			'period_of_stay_start'	: person_object[0].period_of_stay_start,
			'period_of_stay_end'	: person_object[0].period_of_stay_end,
			'reference_person'		: person_object[0].reference_person,
			'remarks'				: person_object[0].remarks
		}
		print person['date_of_birth']
		return render(request, 'HomeInfo/updateForm.html', person)
	elif request.method == 'POST':
		person 					= Person.objects.get(id=1)
		postData				= request.POST
		person 					= Person()
		cursor 					= connection.cursor()
		now 					= datetime.datetime.now()
		current_date 			= now.strftime("%Y-%m-%d")
		person.prefix 			= postData.get('q3_fullName3[prefix]')  
		person.first_name 		= postData.get('q3_fullName3[first]')
		person.middle_name 		= postData.get('q3_fullName3[middle]')
		person.last_name 		= postData.get('q3_fullName3[last]')
		person.registration_date= current_date
		person.house_number 	= postData.get('q22_input22')
		person.house_name 		= postData.get('q23_input23')
		person.land_mark 		= postData.get('q21_address[addr_line1]')
		person.street_address 	= postData.get('q21_address[addr_line2]')
		person.city 			= postData.get('q21_address[city]')
		person.state 			= postData.get('q21_address[state]')
		person.zipcode 			= postData.get('q21_address[postal]')
		person.country 			= postData.get('q21_address[country]')
	
		date_of_birth_not_formated 	= postData.get('Date_of_Birth')
		print(date_of_birth_not_formated)
		if date_of_birth_not_formated != "":
			month,date,year 		= date_of_birth_not_formated.split('/')
			person.date_of_birth 	= str(year) + "-" + str(month) + "-" + str(date)
	
		date_of_death_not_formated 	= postData.get('Date_of_Death')
		if date_of_death_not_formated != "":
			month1,date1,year1 		= date_of_death_not_formated.split('/')
			person.date_of_death 	= str(year1) + "-" + str(month1) + "-" + str(date1)
		
		print person.date_of_death
		person.donation_frequency	= postData.get('q17_donationFrequency')
		person.current_status 	= postData.get('q18_typeA18')
		person.mode_of_communication = postData.get('q19_typeA19')
		person.payment_mode 	= postData.get('q26_typeA26')
		person.reference_person = postData.get('reference_person')
		person.remarks 			= postData.get('q12_suggestionsOr12')
	
	
		person.save()
	
		number_of_phone 		= int(postData.get('number_of_phone')) + 1 
		number_of_landline		= int(postData.get('number_of_landline')) + 1       
		number_of_email 		= int(postData.get('number_of_email')) + 1

		for i in range(1, number_of_phone ):
			phone   					= Phone()
			person_foreignkey_object 	= Person.objects.all().filter(person_id = ID)
			phone.person_id				= person_foreignkey_object[0]
			phone.phone_number  		= postData.get('phone[' + str(i) + '][number]') 
			phone.save()

		for i in range(1, number_of_landline):
			landline 					= Landline()
			person_foreignkey_object 	= Person.objects.all().filter(person_id = ID)
			landline.person_id			= person_foreignkey_object[0]
			landline.landline_number  	= postData.get('landline[' + str(i) + '][number]') 
			landline.save()

		for i in range(1, number_of_email):
			print("hello")
			email 	 					= Email()
			person_foreignkey_object 	= Person.objects.all().filter(person_id = ID)
			email.person_id				= person_foreignkey_object[0]
			email.email_address  		= postData.get('email[' + str(i) + '][number]') 
			email.save()

		for i in range(1, number_of_email):
			print("")
		
		print("person created with id "+person.person_id)
		person_info = {'name': person.prefix +" "+ person.first_name + " "+ person.middle_name + " "+ person.last_name, 'id':person.person_id }
		return render(request, 'HomeInfo/submitSuccess.html', person_info)        
		return render(request, 'HomeInfo/submitSuccess.html')


def product_list(request):
	filter = PersonFilter(request.GET, queryset=Person.objects.all())
	return render(request, 'HomeInfo/search.html', {'filter': filter})

def product_list_sort_by(request, sortBy):
	if sortBy == 'name':
		filter = PersonFilter(request.GET, queryset=Person.objects.order_by('first_name'))
	elif sortBy == 'id':
		filter = PersonFilter(request.GET, queryset=Person.objects.order_by('person_id'))
	elif sortBy == 'period_of_stay':
		filter = PersonFilter(request.GET, queryset=Person.objects.order_by('period_of_stay_start', 'period_of_stay_end'))
	return render(request, 'HomeInfo/search.html', {'filter': filter})


def export_users_xls(request):
	a = request.GET
	print("HIIII")
	print(a.get('id'))
	print(a.get('fn'))
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="users.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['First Name', 'Last Name']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()
	rows = User.objects.all().values_list('first_name', 'last_name')
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response

def transaction(request, id):
	if request.method == 'GET':
		purpose		= Purpose.objects.all()
		person 		= Person.objects.all().filter(person_id = id)
		paymentmode = PaymentMode.objects.all()
		person_info = {'name': person[0].prefix +" "+ person[0].first_name + " "+ person[0].middle_name + " "+ person[0].last_name, 'id':id , 'purposes': purpose, 'paymentmodes': paymentmode}
		return render(request, 'HomeInfo/transaction.html', person_info )
	elif request.method == 'POST':
		transaction					= Transaction()
		postData					= request.POST

		donation_type_and_purpose_id= postData.get('q5_typeA5')
		print(donation_type_and_purpose_id)
		donation_type,purpose_id 	= donation_type_and_purpose_id.split('-')
		print(donation_type + "  " + purpose_id)

		purpose_foreignkey_object	= Purpose.objects.all().filter(purpose_id = purpose_id)
		transaction.donation_purpose_id= purpose_foreignkey_object[0]

		if(donation_type == "Amount"):
			person_foreignkey_object 		= Person.objects.all().filter(person_id = id)
			transaction.person_id			= person_foreignkey_object[0]
			payment_mode_id 					= postData.get('q6_typeA6')
			paymentmode_foreignkey_object 	= PaymentMode.objects.all().filter(payment_mode_id = payment_mode_id)
			transaction.payment_mode_id 	= paymentmode_foreignkey_object[0]
			transaction.receipt_date 		= postData.get('receipt_date')
			receipt_date_not_formated 		= postData.get('receipt_date')
			if receipt_date_not_formated != "":
				month,date,year 			= receipt_date_not_formated.split('/')
				transaction.receipt_date 	= str(year) + "-" + str(month) + "-" + str(date)
			print(transaction.receipt_date)
			transaction.payment_reference   = postData.get('q7_typeA7')
			transaction.receipt_number		= postData.get('q4_typeA')
			transaction.donation_amount 	= postData.get('q9_number')
			transaction.transaction_remarks = postData.get('q8_typeA8')
			transaction.save()
		elif(donation_type == "Other"):
			person_foreignkey_object 		= Person.objects.all().filter(person_id = id)
			transaction.person_id			= person_foreignkey_object[0]
			payment_mode_foreignkey_object  = PaymentMode.objects.all().filter(payment_mode_desc = 'By Hand')
			transaction.payment_mode_id		= payment_mode_foreignkey_object[0]
			transaction.donation_things 	= postData.get('q10_typeA10')
			transaction.transaction_remarks = postData.get('q8_typeA8')
			transaction.save()
		return render(request, 'HomeInfo/transactionsuccess.html', { 'id': id})

def purpose(request):
	if request.method == 'GET':
		return render(request, 'HomeInfo/purpose.html')
	elif request.method == 'POST':
		purpose 				= Purpose()
		postData				= request.POST
		purpose.purpose_id 		= postData.get('q3_name')
		purpose.donation_type	= postData.get('q18_typeA18')
		purpose.purpose_desc	= postData.get('q4_email')
		purpose.purpose_remarks = postData.get('q6_message')
		purpose.save()
		return render(request, 'HomeInfo/submitSuccess.html', {'value': 1})



def paymentmode(request):
	if request.method == 'GET':
		return render(request, 'HomeInfo/paymentmode.html')
	elif request.method == 'POST':
		postData						= request.POST
		paymentmode 					= PaymentMode()
		paymentmode.payment_mode_id		= postData.get('q3_name')
		paymentmode.payment_mode_desc	= postData.get('q4_email')
		paymentmode.payment_mode_remarks= postData.get('q6_message')
		paymentmode.save()
		return render(request, 'HomeInfo/paymentmodesuccess.html')


@csrf_exempt
def profile(request, id):
	# postData 			= request.POST
	# person_ids_unicode 	= postData.getlist('person_ids[]')
	# person_ids 			= []
	# for person_i in person_ids_unicode:
	# 	person_ids.append(str(person_i))
	# print person_ids

	person_object		= Person.objects.all().filter(person_id = id)
	transaction_object  = Transaction.objects.all().filter(person_id = id)
	transaction_list    = []
	for i in transaction_object:
		transaction 				= []
		purpose 					= i.donation_purpose_id
		purpose_id    				= purpose.purpose_id
		transaction_purpose 		= Purpose.objects.all().filter(purpose_id = purpose_id)
		transaction_doantion_type	= transaction_purpose[0].donation_type
		transaction_doantion_disc	= transaction_purpose[0].purpose_desc
		transaction.append(transaction_doantion_type)
		payment_mode 				= i.payment_mode_id
		payment_mode_id				= payment_mode.payment_mode_id
		transaction_payment			= PaymentMode.objects.all().filter(payment_mode_id = payment_mode_id)
		transaction_payment_mode_disc= transaction_payment[0].payment_mode_desc
		transaction.append(transaction_payment_mode_disc)
		transaction.append(i.receipt_date)
		transaction.append(i.receipt_number)
		transaction.append(i.donation_amount)
		transaction.append(i.donation_things)
		transaction.append(i.payment_reference)
		transaction.append(purpose_id)
		transaction.append(transaction_doantion_disc)
		transaction_list.append(transaction)


	phone_object 		= Phone.objects.all().filter(person_id = id)
	phone_list			= []
	for i in phone_object:
		phone_list.append(i.phone_number)

	landline_object 	= Landline.objects.all().filter(person_id = id)
	landline_list		= []
	for i in landline_object:
		landline_list.append(i.landline_number)

	email_object 		= Email.objects.all().filter(person_id = id)
	email_list			= []
	for i in email_object:
		email_list.append(i.email_address)

	person = {
				'name' : person_object[0].prefix + " " + person_object[0].first_name + " " + person_object[0].middle_name + " " + person_object[0].last_name,
				'id'   : person_object[0].person_id,
				'date_of_birth' : person_object[0].date_of_birth,
				'house_number'			: person_object[0].house_number,
				'house_name'			: person_object[0].house_name,
				'land_mark' 			: person_object[0].land_mark,
				'street_address'		: person_object[0].street_address,
				'city'					: person_object[0].city,
				'state'					: person_object[0].state,
				'zipcode'    			: person_object[0].zipcode,
				'country' 				: person_object[0].country,
				'phone'					: phone_list,
				'landline'				: landline_list,
				'email'					: email_list,
				'mode_of_communication' : person_object[0].mode_of_communication,
				'period_of_stay_start'	: person_object[0].period_of_stay_start,
				'period_of_stay_end'    : person_object[0].period_of_stay_end,
				'reference_person'		: person_object[0].reference_person,
				'transaction'			: transaction_list,
				'address'				: person_object[0].street_address + ", " + person_object[0].city + ", " + person_object[0].state
		}
	return render(request, 'HomeInfo/profile.html', person)


@csrf_exempt
def profile_post_data(request, id):
	postData 			= request.POST
	person_ids_unicode 	= postData.getlist('person_ids[]')
	person_ids 			= []
	for person_i in person_ids_unicode:
		person_ids.append(str(person_i))
	print person_ids

	person_object		= Person.objects.all().filter(person_id = id)
	transaction_object  = Transaction.objects.all().filter(person_id = id)
	transaction_list    = []
	for i in transaction_object:
		transaction 				= []
		purpose 					= i.donation_purpose_id
		purpose_id    				= purpose.purpose_id
		transaction_purpose 		= Purpose.objects.all().filter(purpose_id = purpose_id)
		transaction_doantion_type	= transaction_purpose[0].donation_type
		transaction_doantion_disc	= transaction_purpose[0].purpose_desc
		transaction.append(transaction_doantion_type)
		payment_mode 				= i.payment_mode_id
		payment_mode_id				= payment_mode.payment_mode_id
		transaction_payment			= PaymentMode.objects.all().filter(payment_mode_id = payment_mode_id)
		transaction_payment_mode_disc= transaction_payment[0].payment_mode_desc
		transaction.append(transaction_payment_mode_disc)
		transaction.append(i.receipt_date)
		transaction.append(i.receipt_number)
		transaction.append(i.donation_amount)
		transaction.append(i.donation_things)
		transaction.append(i.payment_reference)
		transaction.append(purpose_id)
		transaction.append(transaction_doantion_disc)
		transaction_list.append(transaction)


	phone_object 		= Phone.objects.all().filter(person_id = id)
	phone_list			= []
	for i in phone_object:
		phone_list.append(i.phone_number)

	landline_object 	= Landline.objects.all().filter(person_id = id)
	landline_list		= []
	for i in landline_object:
		landline_list.append(i.landline_number)

	email_object 		= Email.objects.all().filter(person_id = id)
	email_list			= []
	for i in email_object:
		email_list.append(i.email_address)

	person = {
				'name' : person_object[0].prefix + " " + person_object[0].first_name + " " + person_object[0].middle_name + " " + person_object[0].last_name,
				'id'   : person_object[0].person_id,
				'date_of_birth' : person_object[0].date_of_birth,
				'house_number'			: person_object[0].house_number,
				'house_name'			: person_object[0].house_name,
				'land_mark' 			: person_object[0].land_mark,
				'street_address'		: person_object[0].street_address,
				'city'					: person_object[0].city,
				'state'					: person_object[0].state,
				'zipcode'    			: person_object[0].zipcode,
				'country' 				: person_object[0].country,
				'phone'					: phone_list,
				'landline'				: landline_list,
				'email'					: email_list,
				'mode_of_communication' : person_object[0].mode_of_communication,
				'period_of_stay_start'	: person_object[0].period_of_stay_start,
				'period_of_stay_end'    : person_object[0].period_of_stay_end,
				'reference_person'		: person_object[0].reference_person,
				'transaction'			: transaction_list,
				'address'				: person_object[0].street_address + ", " + person_object[0].city + ", " + person_object[0].state,
				'person_ids'			: person_ids
		}
	return render(request, 'HomeInfo/profile_post_data.html', person)

def features(request):
	return render(request, 'HomeInfo/features.html')

def report(request):
	return render(request, 'HomeInfo/report.html')

def card(request):
	filter = PersonFilter(request.GET, queryset=Person.objects.all())
	return render(request, 'HomeInfo/card.html', {'filter': filter})

def card_sort_by(request, sortBy):
	if sortBy == 'name':
		filter = PersonFilter(request.GET, queryset=Person.objects.order_by('first_name'))
	elif sortBy == 'id':
		filter = PersonFilter(request.GET, queryset=Person.objects.order_by('person_id'))
	elif sortBy == 'period_of_stay':
		filter = PersonFilter(request.GET, queryset=Person.objects.order_by('period_of_stay_start', 'period_of_stay_end'))
	return render(request, 'HomeInfo/card.html', {'filter': filter})

def emailList(request):
	filter = PersonFilter(request.GET, queryset=Person.objects.all())
	return render(request, 'HomeInfo/emailList.html', {'filter': filter})


def quick_search_id(request):
	ID = request.POST.get('id')
	persons = Person.objects.filter(person_id__icontains=ID)

	if len(persons) == 1:
		person_id = persons[0].person_id
		return redirect("/Home/profile/"+person_id)

	return render(request, 'HomeInfo/quick_search.html', {'persons': persons})


def quick_search_name(request):
	name = request.POST.get('name')
	queryset = Person.objects.annotate(full_name=Concat('first_name', Value(' '),'middle_name', Value(' '), 'last_name'))
	persons = queryset.filter(full_name__icontains=name)

	if len(persons) == 1:
		person_id = persons[0].person_id
		return redirect("/Home/profile/"+person_id)

	return render(request, 'HomeInfo/quick_search.html', {'persons': persons})