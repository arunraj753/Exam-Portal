from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import user_is_teacher,user_is_student,user_is_creator
from .models import Exam,Question,Option,Candidate,ExamStatus
from .forms import (ExamCreateForm,QuestionCreationForm,
	OptionCreationForm,ExamAttendForm,
	OptionUpdateForm)
from django.core.paginator import Paginator
from django.db.models import Sum
@login_required
def home(request):
	if request.user.is_student == True:
		return redirect("/home/student")
	elif request.user.is_teacher==True: 
		return redirect("/home/teacher")
	return HttpResponse("Invalid")
@user_is_teacher
def home_teacher(request):
	exams=Exam.objects.filter(exam_creator=request.user)
	context={'exams':exams}
	return render(request,"examonline/examslist.html",context)
@user_is_student
def home_student(request):
	exams=Exam.objects.all()
	examstats=ExamStatus.objects.filter(stud_name=request.user)
	context={'exams':exams,'examstats':examstats}
	return render(request,"examonline/studenthome.html",context)

@login_required
@user_is_teacher
def ExamCreateView(request):
	if request.method=='POST':	
		form=ExamCreateForm(request.POST)
		form.instance.exam_creator=request.user
		if form.is_valid():
			form.save()
		return redirect('/home/teacher')
	form=ExamCreateForm()
	context={'form':form}
	return render(request,'examonline/examcreate.html',context)

@login_required
@user_is_teacher
def QuestionCreateView(request):
	if request.method=='POST':
		form=QuestionCreationForm(request.POST)
		return HttpResponse("Question Created")
	form=QuestionCreationForm()
	context={'form':form}
	return render(request,'examonline/questioncreate.html',context)
@login_required
@user_is_teacher
@user_is_creator
def ExamDetailsView(request,pk):
	idd=pk
	Exam_Object=Exam.objects.get(pk=pk)
	questions=Question.objects.filter(question_exam=Exam_Object)
	if Question.objects.filter(question_exam=Exam_Object):
		TotalMarks=Question.objects.filter(question_exam=Exam_Object).aggregate(Sum('question_mark'))
		Exam_Object.exam_marks=TotalMarks.get('question_mark__sum')
		Exam_Object.save() 
	if request.method=='POST':

		form=QuestionCreationForm(request.POST,request.FILES)

		form.instance.question_creator=request.user
		form.instance.question_exam=Exam_Object
		if form.is_valid():
			ques_ob=form.save()
			print(ques_ob.pk)
			return redirect('/question/'+str(ques_ob.pk)+'/option/create')
	form=QuestionCreationForm()
	context={'form':form,'questions':questions,'exam':Exam_Object}
	return render(request,'examonline/examdetails.html',context)
@login_required


def OptionCreateView(request,pk):
	idd=pk
	print("id of question is ",idd)
	Question_Object=Question.objects.get(pk=pk)
	print("Question object is",Question_Object)
	if request.method=='POST':
		form=OptionCreationForm(request.POST)
		form.instance.question=Question_Object
		form.save()
		return redirect('/question/'+str(pk)+'/option/create')
	form=OptionCreationForm()
	options=Question_Object.option_set.all()
	print(Question_Object.option_set.all())
	context={'form':form,'question':Question_Object,'options':options}#,'ca_form':ca_form}
	return render(request,'examonline/optioncreate.html',context)

def TrueOption(request,pk):
	TrueOption=Option.objects.get(pk=pk)
	id=TrueOption.question.pk
	Question_Object=Question.objects.get(pk=id)
	Question_Object.option_set.all().update(option_status=False)
	TrueOption.option_status=True
	TrueOption.save()
	return redirect('/question/'+str(id)+'/option/create')
	

def ExamPreview(request,pk):
	Exam_Object=Exam.objects.get(pk=pk)
	questions=Exam_Object.question_set.all()
	print(questions)
	context ={'questions':questions}
	return render(request,'examonline/exampreview.html',context)
def ExamEditView(request,pk):
	Exam_Object=Exam.objects.get(pk=pk)
	form=ExamCreateForm(request.POST or None,instance=Exam_Object)
	context={'form':form}
	if request.method=='POST':
		if form.is_valid():
			form.save()
			return redirect('/home/teacher')
	return render(request,'examonline/examedit.html',context)
def ExamDeleteView(request,pk):
	Exam_Object=Exam.objects.get(pk=pk)
	context={'exam':Exam_Object}
	if request.method=='POST':
		Exam_Object.delete()
		return redirect('/home/teacher')
	return render(request,'examonline/examdelete.html',context)
def QuestionEditView(request,pk):
	QuestionObject=Question.objects.get(pk=pk)
	form=QuestionCreationForm(request.POST or None, instance=QuestionObject)
	if(request.method=='POST'):
		if form.is_valid():
			form.save()
			id=QuestionObject.question_exam.pk
			return redirect('/exam/'+str(id)+'/details')
	context={'form':form}
	return render(request,'examonline/questioncreate.html',context)
def QuestionDeleteView(request,pk):
	QuestionObject=Question.objects.get(pk=pk)
	context={'question':QuestionObject}
	if request.method=='POST':
		QuestionObject.delete()
		return redirect('/home/teacher')
	return render(request,'examonline/questiondelete.html',context)

def OptionDeleteView(request,pk):
	OptionObject=Option.objects.get(pk=pk)
	id=OptionObject.question.pk
	OptionObject.delete()
	return redirect('/question/'+str(id)+'/option/create')


def ExamGuidelinesView(request,pk):
	ExamObject=Exam.objects.get(pk=pk)
	StatusQuery=ExamStatus.objects.all()
	if StatusQuery.filter(stud_name=request.user).filter(test=ExamObject):
		print(StatusQuery)
		ExamStatusObject=StatusQuery.filter(stud_name=request.user).get(test=ExamObject)
		print(ExamStatusObject)
		if ExamStatusObject.exam_status==True:
			return render(request,'examonline/alreadyattempted.html')
	else:
		ExamStatusObject=ExamStatus()
		ExamStatusObject.stud_name=request.user
		ExamStatusObject.test=ExamObject
		ExamStatusObject.timeleft=ExamObject.exam_time*60
		ExamStatusObject.save()
	context={'exam':ExamObject,'status':ExamStatusObject}
	return render(request,'examonline/examguidelines.html',context)

def ExamConfirmSubmit(request,pk):
	context={'pk':pk}
	return render(request,'examonline/confirm.html',context)

def ExamSubmitView(request,pk):
	ExamSubmitObject=ExamStatus()
	ExamSubmitObject.test=Exam.objects.get(pk=pk)
	ExamSubmitObject.stud_name=request.user
	ExamSubmitObject.exam_status=True
	CandidateMarks=Candidate.objects.filter(stud_name=request.user).filter(stud_exam=ExamSubmitObject.test).aggregate(Sum('stud_mark'))

	mark=CandidateMarks.get('stud_mark__sum')
	#TotalMarks=Question.objects.filter(question_exam=Exam_Object).aggregate(Sum('question_mark'))
	#Exam_Object.exam_marks=TotalMarks.get('question_mark__sum')
	#Exam_Object.save() 
	context={'mark':mark}
	#return HttpResponse(pk)
	return render(request,'examonline/result.html',context)
def ImageAdd(request):
	form = TrialForm() 
	context={'form':form}
	if request.method=='POST':
		form=TrialForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			print("Valid")
			print(form)
			return redirect('success')
	return render(request,'examonline/addimage.html',context)

def hotel_image_view(request): 
  
    if request.method == 'POST': 
        form = HotelForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = HotelForm() 
    return render(request, 'examonline/hotel_image_form.html', {'form' : form}) 
  
def TrialAttend(request,pk):
	print(pk)
	Exam_Object=Exam.objects.get(pk=pk)
	print(Exam_Object)
	ExamStatusObject=ExamStatus.objects.filter(stud_name=request.user).get(test=Exam_Object)
	questions=Exam_Object.question_set.all()
	ExamObject=Exam.objects.get(pk=pk)
	Estat=ExamStatus.objects.filter(stud_name=request.user).get(test=Exam_Object)
	runtime=Estat.timeleft
	Attempted=Candidate.objects.filter(stud_name=request.user).filter(stud_exam=Exam_Object)
	paginator=Paginator(questions,1)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	q=paginator.page_range
	p=paginator.page(paginator.num_pages)
	if request.method=='GET':
		del_option=request.GET.get('del')
		if del_option !=None:
			page_obj = paginator.get_page(del_option)
			CandidateObject=Candidate.objects.filter(stud_name=request.user).filter(stud_question=questions[page_obj.number-1])
			CandidateObject.delete()
		upruntime=(request.GET.get('time'))
		if upruntime != None:	
			Estat.timeleft=int(upruntime)	
			print(Estat)
			Estat.save()
	form=ExamAttendForm()
	form.fields["stud_option"].queryset=Option.objects.filter(question=questions[page_obj.number-1])
	if (Attempted.filter(stud_question=questions[page_obj.number-1])):
		CandidateObject=Candidate.objects.filter(stud_name=request.user).filter(stud_question=questions[page_obj.number-1])
		form=ExamAttendForm(request.POST or None,instance=CandidateObject[0])
		form.fields["stud_option"].queryset=Option.objects.filter(question=questions[page_obj.number-1])
	#else:
	#	form=ExamAttendForm(request.POST or None,instance=CandidateObject[0])
	#	form.fields["stud_option"].queryset=Option.objects.filter(question=questions[page_obj.number-1])
	if (request.method=='POST'):
		if (Attempted.filter(stud_question=questions[page_obj.number-1])):
			CandidateObject=Candidate.objects.filter(stud_name=request.user).filter(stud_question=questions[page_obj.number-1])
			form=ExamAttendForm(request.POST or None,instance=CandidateObject[0])
		else:
			form=ExamAttendForm(request.POST)
		form.fields["stud_option"].queryset=Option.objects.filter(question=questions[page_obj.number-1])
		form.instance.stud_name=request.user
		form.instance.stud_exam=Exam_Object
		form.instance.stud_question=questions[page_obj.number-1]
		OptionObject=Option.objects.filter(question=questions[page_obj.number-1]).get(option_status=True)
		if form.is_valid():
			try:
				form.save()
				if OptionObject==form.instance.stud_option:
					form.instance.stud_mark=questions[page_obj.number-1].question_mark
					if form.is_valid():
						form.save()
				else:
					form.instance.stud_mark=-1*questions[page_obj.number-1].question_negative
					form.save()
			except:pass
		if page_obj.has_next() == True:
			return redirect("/exam/"+str(pk)+"/trial?page="+str(page_obj.next_page_number()))
		else:
			return redirect("/exam/"+str(pk)+"/trial?page="+str(page_obj.previous_page_number()))

	AttemptedQuestions=[]
	for i in q:
		new_obj = paginator.get_page(i)
		if (Attempted.filter(stud_question=questions[new_obj.number-1])):
			AttemptedQuestions.append(i)
	print("Attempted questin numbers are ",AttemptedQuestions)
	context={'paginator':paginator,'runtime':runtime,'q':q,'AttemptedQuestions':AttemptedQuestions,'page_obj':page_obj,'form':form,}#,'page_object':page_object}
	print("Pk at last is ",pk)
	return render(request,'examonline/trialattend3.html',context)
	
def ExamAttend(request,pk):
	print("Next or Prev Clicked")
	Exam_Object=Exam.objects.get(pk=pk)
	ExamStatusObject=ExamStatus.objects.filter(stud_name=request.user).get(test=Exam_Object)
	time=ExamStatusObject.timeleft
	print(ExamStatusObject)
	Attempted=Candidate.objects.filter(stud_name=request.user).filter(stud_exam=Exam_Object)
	questions=Exam_Object.question_set.all()
	paginator = Paginator(questions, 1)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	if request.method=='GET':
		timeleft=request.GET.get('time')
	form=ExamAttendForm()
	form.fields["stud_option"].queryset=Option.objects.filter(question=questions[page_obj.number-1])
	if (Attempted.filter(stud_question=questions[page_obj.number-1])):
		CandidateObject=Candidate.objects.filter(stud_name=request.user).filter(stud_question=questions[page_obj.number-1])
		form=ExamAttendForm(request.POST or None,instance=CandidateObject[0])
		form.fields["stud_option"].queryset=Option.objects.filter(question=questions[page_obj.number-1])
		form=ExamAttendForm(request.POST or None, instance=CandidateObject[0])
		form.fields['stud_option'].queryset=Option.objects.filter(question=questions[page_obj.number-1])
	if (request.method=='POST'):
		if (Attempted.filter(stud_question=questions[page_obj.number-1])):
			CandidateObject=Candidate.objects.filter(stud_name=request.user).filter(stud_question=questions[page_obj.number-1])
			form=ExamAttendForm(request.POST or None,instance=CandidateObject[0])
		else:
			form=ExamAttendForm(request.POST)
		form.fields["stud_option"].queryset=Option.objects.filter(question=questions[page_obj.number-1])
		form.instance.stud_name=request.user
		form.instance.stud_exam=Exam_Object
		form.instance.stud_question=questions[page_obj.number-1]
		OptionObject=Option.objects.filter(question=questions[page_obj.number-1]).get(option_status=True)
		print("Correct Option is",OptionObject)
		if form.is_valid():
			form.save()
		print("user option is ",form.instance.stud_option)
		if OptionObject==form.instance.stud_option:
			print("Correct Answer")
			form.instance.stud_mark=questions[page_obj.number-1].question_mark
			if form.is_valid():
				form.save()
		else:
			form.instance.stud_mark=-1*questions[page_obj.number-1].question_negative
			form.save()
	context={'page_obj': page_obj,'form':form,'exam':Exam_Object,'time':time}
	return render(request,'examonline/examattend.html',context)