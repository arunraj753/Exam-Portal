from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .forms import UserRegisterForm
from .decorators import user_is_student,user_is_teacher
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Password Change Successful')
            return redirect('home')
        #else:
         #   messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/passwordchange.html', {
        'form': form
    })	      

def student_registration(request):
	if request.method=='POST':
		form=UserRegisterForm(request.POST)
		if form.is_valid():
			print("Valid Function , details can be saved")
			user=form.save(commit=False)
			user.is_student=True
			user.is_active = False
			user.save()
			context={'name':user.first_name}
			messages.success(request, 'Success !!')
			return render(request,'accounts/regsuccess.html',context)
            
	else:
		form=UserRegisterForm()
	context={'form':form,'usertype':'Student'}
	return render(request,'accounts/register.html',context)

def teacher_registration(request):
	if request.method=='POST':
		form=UserRegisterForm(request.POST)
		if form.is_valid():
			print("Valid Function , details can be saved")
			user=form.save(commit=False)
			user.is_teacher=True
			user.is_active = False
			user.save()
			context={'name':user.first_name}
			messages.success(request, 'Your Account Created successfully')
			return render(request,'accounts/regsuccess.html',context)

            
	else:
		form=UserRegisterForm()
	context={'form':form,'usertype':'Teacher'}
	return render(request,'accounts/register.html',context)

def index(request):
	return HttpResponse("Hello this is home")
@login_required
def account(request):
	return render(request,'accounts/account.html')
@login_required
@user_is_teacher
def tview(request):
	return HttpResponse("This page is for teacher")

@login_required
@user_is_student
def sview(request):
	return HttpResponse("this page is for student")



