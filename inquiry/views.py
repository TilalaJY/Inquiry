from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, View
from django.views.generic.base import TemplateView
from .models import *
from .forms import *
import random
import requests
import phonenumbers
import datetime
from django.http import HttpResponse
from django.contrib import messages 



class InquiryListView(ListView):
    model = Inquiry
    template_name = "inquiry/list.html"

def send_otp(number,message):
    url = "https://www.fast2sms.com/dev/bulk"
    api = "xwVgJYIyRkGj8d4HXfb3O9Np7L20PWnTtCuBvDSU5KAar6QMlirzBqXlDGFcEodb4Au7n5HjkLv8M6e2"
    querystring = {"authorization":api,"sender_id":"FSTSMS","message":message,"language":"english","route":"p","numbers":str(number)}
    headers = {
        'cache-control': "no-cache"
    }
    return requests.request("GET", url, headers=headers, params=querystring)

class InquiryRegisteration(View):
    # model = Inquiry
    # # fields = "__all__"
    # template_name = "inquiry/create.html"
    # form_class = InquiryForms

    template_name = "inquiry/create.html"

    def get(self, request):
        return render(request, self.template_name, {"form": InquiryForms()})

    def post(self, request):
        form = InquiryForms(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            email = form.cleaned_data['email']
            phone_no = int(form.cleaned_data['phone_no'].national_number)
            if form.cleaned_data['product_end_date'] < form.cleaned_data['product_start_date']:
                raise forms.ValidationError("End date should be greater than start date.")
            product_end_date = datetime.datetime.strftime( form.cleaned_data['product_end_date'], "%Y-%m-%d")
            product_start_date = datetime.datetime.strftime( form.cleaned_data['product_start_date'], "%Y-%m-%d")
            complain_message = form.cleaned_data['complain_message']
            request.session['customer_name'] = customer_name
            request.session['email'] = email
            request.session['phone_no'] = phone_no
            request.session['product_end_date'] = product_end_date
            request.session['product_start_date'] = product_start_date
            request.session['complain_message'] = complain_message
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
            message = f'your otp is {otp}'
            send_otp(phone_no, message)
            return redirect('otp-Registration')


        return render(request,self.template_name, {"form": form})


class InquiryotpRegistration(View):
    template_name = "inquiry/otp-registration.html"
    def get(self, request):
        return render(request, "inquiry/otp-registration.html", {})

    def post(self, request):
        user_otp = request.POST['otp']
        otp = request.session.get('otp')
        customer_name = request.session.get("customer_name")
        email = request.session.get('email')
        phone_no = phonenumbers.parse("+91"+str(request.session.get('phone_no')))
        product_end_date = datetime.datetime.strptime(request.session.get('product_end_date'), "%Y-%m-%d")
        product_start_date = datetime.datetime.strptime(request.session.get('product_start_date'), "%Y-%m-%d")
        complain_message = request.session.get('complain_message')

        if int(user_otp) == otp:
            Inquiry.objects.create(
                customer_name = customer_name,
                email = email,
                phone_no = phone_no,
                product_end_date = product_end_date,
                product_start_date = product_start_date,
                complain_message = complain_message,
            )
            request.session.delete('email')
            request.session.delete('email')
            request.session.delete('number')
            request.session.delete('product_end_date')
            request.session.delete('product_start_date')
            request.session.delete('complain_message')
            request.session.delete('phone_no')
            request.session.delete('phone_no')
            request.session.delete('otp')

            return redirect("InquiryList")
        else:
            messages.error(request,'Wrong OTP')
        return render(request,self.template_name)


