from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from accounts.decorators import (user_is_teacher,user_is_student,
	user_is_examcreator,user_is_questioncreator,user_is_optioncreator)
from .models import Exam,Question,Option,Candidate,ExamStatus
from accounts.models import Student,User
from .forms import (ExamCreateForm,QuestionCreationForm,
	OptionCreationForm,ExamAttendForm,
	OptionUpdateForm)
from django.core.paginator import Paginator
from django.db.models import Sum
from itertools import chain
@login_required
def AdminHome(request):
	if request.user.is_superuser == True:
		exams=Exam.objects.all().order_by('exam_creator')
	else:
		raise PermissionDenied
	context={'exams':exams}
	return render (request,'examonline/adminhome.html',context)

@login_required
def home(request):
	if request.user.is_student == True:
		return redirect("/home/student")
	elif request.user.is_teacher==True: 
		return redirect("/home/teacher")
	return HttpResponse("Invalid")

###############  Teacher Views ############### 
@login_required
@user_is_teacher
def home_teacher(request):
	postedexams=Exam.objects.filter(exam_creator=request.user).filter(exam_ready=True)
	exams=Exam.objects.filter(exam_creator=request.user).filter(exam_ready=False)
	print(postedexams)
	print(exams)
	context={'postedexams':postedexams,'exams':exams}
	return render(request,"examonline/examslist.html",context)

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
@user_is_examcreator
def ExamDetailsView(request,pk):
	idd=pk
	Exam_Object=Exam.objects.get(pk=pk)
	questions=Question.objects.filter(question_exam=Exam_Object)
	if request.method=='POST':
		form=QuestionCreationForm(request.POST,request.FILES)
		form.instance.question_creator=request.user
		form.instance.question_exam=Exam_Object
		if form.is_valid():
			ques_ob=form.save()
			if questions:
				TotalMarks=Question.objects.filter(question_exam=Exam_Object).aggregate(Sum('question_mark'))
				Exam_Object.exam_marks=TotalMarks.get('question_mark__sum')
				Exam_Object.save() 
				print("OK")
				print(Exam_Object.pk)
				print(ques_ob.pk)
			return redirect('/question/'+str(ques_ob.pk)+'/option/create')
	form=QuestionCreationForm()
	context={'form':form,'questions':questions,'exam':Exam_Object}
	return render(request,'examonline/examdetails.html',context)

@login_required
@user_is_examcreator
def ExamEditView(request,pk):
	Exam_Object=Exam.objects.get(pk=pk)
	form=ExamCreateForm(request.POST or None,instance=Exam_Object)
	context={'form':form}
	if request.method=='POST':
		if form.is_valid():
			form.save()
			return redirect('/home/teacher')
	return render(request,'examonline/examedit.html',context)

@login_required
@user_is_examcreator
def ExamUpdate(request,pk):
	ExamObject=Exam.objects.get(pk=pk)
	questions=ExamObject.question_set.all()
	paginator=Paginator(questions,1)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	print(page_obj.number)
	q=paginator.page_range
	context={'q':q,'page_obj':page_obj,'questions':questions}
	return render(request,'examonline/examupdate.html',context)

@login_required
@user_is_examcreator
def ExamDeleteView(request,pk):
	Exam_Object=Exam.objects.get(pk=pk)
	context={'exam':Exam_Object}
	if request.method=='POST':
		Exam_Object.delete()
		return redirect('/home/teacher')
	return render(request,'examonline/examdelete.html',context)

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
@user_is_questioncreator
def QuestionEditView(request,pk):
	QuestionObject=Question.objects.get(pk=pk)
	Exam_Object=QuestionObject.question_exam
	Emarks=Exam_Object.exam_marks
	Qmark=QuestionObject.question_mark
	form=QuestionCreationForm(request.POST or None,request.FILES or None,instance=QuestionObject)
	if request.method=='POST':
		form=QuestionCreationForm(request.POST,request.FILES)
		form.instance.question_creator=request.user
		form.instance.question_exam=Exam_Object
		if form.is_valid():
			Exam_Object
			QuestionObject.question_image=(form.cleaned_data['question_image'])
			QuestionObject.question=(form.cleaned_data['question'])
			QuestionObject.question_negative=(form.cleaned_data['question_negative'])
			QuestionObject.question_mark=(form.cleaned_data['question_mark'])
			QuestionObject.save()
			Exam_Object.exam_marks=Emarks-Qmark+QuestionObject.question_mark
			Exam_Object.save()
			#ques_ob=form.save()
			return redirect('/exam/'+str(Exam_Object.pk)+'/update')
	context={'form':form,'ques':QuestionObject,'exam':Exam_Object}
	return render(request,'examonline/questionupdate.html',context)
@login_required
@user_is_questioncreator
def QuestionDeleteView(request,pk):
	QuestionObject=Question.objects.get(pk=pk)
	exam=QuestionObject.question_exam
	mark=exam.exam_marks
	qmark=QuestionObject.question_mark
	id=exam.pk
	context={'question':QuestionObject}
	if request.method=='POST':
		QuestionObject.delete()
		exam.exam_marks=mark-qmark
		exam.save()
		return redirect('/exam/'+str(id)+'/update')
	return render(request,'examonline/questiondelete.html',context)

@login_required
@user_is_questioncreator
def OptionCreateView(request,pk):
	print("in option")
	idd=pk
	print("In option ")
	Question_Object=Question.objects.get(pk=pk)

	if request.method=='POST':
		form=OptionCreationForm(request.POST)
		form.instance.question=Question_Object
		form.save()
		return redirect('/question/'+str(pk)+'/option/create')
	form=OptionCreationForm()
	options=Question_Object.option_set.all()
	context={'form':form,'question':Question_Object,'options':options}#,'ca_form':ca_form}
	return render(request,'examonline/optioncreate.html',context)

@login_required
@user_is_optioncreator
def TrueOption(request,pk):
	TrueOption=Option.objects.get(pk=pk)
	id=TrueOption.question.pk
	Question_Object=Question.objects.get(pk=id)
	Question_Object.option_set.all().update(option_status=False)
	TrueOption.option_status=True
	TrueOption.save()
	return redirect('/question/'+str(id)+'/option/create')

@login_required
@user_is_optioncreator
def OptionDeleteView(request,pk):
	OptionObject=Option.objects.get(pk=pk)
	id=OptionObject.question.pk
	OptionObject.delete()
	return redirect('/question/'+str(id)+'/option/create')

@login_required
@user_is_examcreator
def ExamPost(request,pk):
	ExamObject=Exam.objects.get(pk=pk)
	questions=Question.objects.filter(question_exam=ExamObject)
	qcount=questions.count()
	for q in questions:
		opt=q.option_set.all()
		optcount=opt.count()
		if(opt.exists()):
			if optcount<3:
				context={'optcount':optcount,'ques':q}
				return render(request,'examonline/fewoptions.html',context)
			if Option.objects.filter(question=q).filter(option_status=True).exists():
				pass
			else:
				context={'ques':q}
				return render(request,'examonline/examoptionsubmitfail.html',context)
		else:
			context={'ques':q}
			return render(request,'examonline/examsubmitfail.html',context)
	if (qcount<5):
		context={'qcount':qcount,'exampk':pk}
		return render (request,'examonline/fewquestions.html',context)
	ExamObject.exam_ready=True
	ExamObject.save()
	return redirect('/')

@login_required
@user_is_examcreator
def ExamPreviewPaginated(request,pk):
	ExamObject=Exam.objects.get(pk=pk)
	questions=ExamObject.question_set.all()
	paginator=Paginator(questions,1)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	print(page_obj.number)
	q=paginator.page_range
	context={'q':q,'page_obj':page_obj,'questions':questions}
	return render(request,'examonline/exampreviewpaginated.html',context)

@login_required
@user_is_examcreator
def AnswerPaper(request,pk,spk):
	ExamObject=Exam.objects.get(pk=pk)
	stud=User.objects.get(pk=spk)
	ExamStatusObject=ExamStatus.objects.filter(stud_name=stud).get(test=ExamObject)
	if ExamStatusObject.exam_status == False:
		raise PermissionDenied
	else:
		questions=ExamObject.question_set.all()
		Attempted=Candidate.objects.filter(stud_name=stud).filter(stud_exam=ExamObject)
		paginator=Paginator(questions,1)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		print(page_obj.number)
		q=paginator.page_range
		try:
			StudOption=Candidate.objects.filter(stud_name=stud).get(stud_question=page_obj[0])
		except:
			StudOption=[]
		context={'paginator':paginator,'q':q,'page_obj':page_obj,'questions':questions,'attempted':Attempted,'studoption':StudOption}
		return render(request,'examonline/examsolutionpaginated.html',context)

@login_required
@user_is_examcreator
def Rank(request,pk):
	ExamObject=Exam.objects.get(pk=pk)
	students=ExamStatus.objects.filter(test=ExamObject).filter(exam_status=True).order_by('-exam_marks')
	c=students.count()
	for i in students:
		pass
	for i in range(0,c):
		if i == 0:
			students[i].rank=i+1
		elif i!=0 and students[i].exam_marks == students[i-1].exam_marks:
			students[i].rank=students[i-1].rank	
		else:
			students[i].rank=students[i-1].rank+1
		if(students[i].exam_marks >= ExamObject.exam_passmark):
			students[i].save()
		else:
			students[i].rank=-1
			students[i].save()
	context={'students':students}
	return render(request,'examonline/rank.html',context)

@login_required
@user_is_examcreator
def PassMark(request,pk):
	ExamObject=Exam.objects.get(pk=pk)
	if (request.method=='POST'):
		value=int(request.POST["pass"])
		ExamObject.exam_passmark=value
		ExamObject.save()
		return redirect("/")		
	return render(request,'examonline/passmark.html',{'exam':ExamObject})

###############  Student Views ############### 

@login_required
@user_is_student
def home_student(request):
	pending=ExamStatus.objects.filter(stud_name=request.user).filter(test__exam_ready=True).filter(exam_status=False)
	completed=ExamStatus.objects.filter(stud_name=request.user).filter(exam_status=True)
	modfiedstatus=ExamStatus.objects.filter(stud_name=request.user).values('test')
	unattempted = Exam.objects.filter(exam_ready=True).exclude(id__in=modfiedstatus)
	context={'unattempted':unattempted,'completed':completed,'pending':pending}
	return render(request,"examonline/studenthome.html",context)
@login_required
@user_is_student
def ExamGuidelinesView(request,pk):
	ExamObject=Exam.objects.get(pk=pk)
	#StatusQuery=ExamStatus.objects.all()
	if ExamStatus.objects.filter(stud_name=request.user).filter(test=ExamObject):
		ExamStatusObject=ExamStatus.objects.filter(stud_name=request.user).get(test=ExamObject)
		if ExamStatusObject.exam_status==True:
			context={'ExamStatusObject':ExamStatusObject}
			return render(request,'examonline/alreadyattempted.html',context)
	else:
		ExamStatusObject=ExamStatus()
		ExamStatusObject.stud_name=request.user
		ExamStatusObject.test=ExamObject
		ExamStatusObject.timeleft=ExamObject.exam_time*60
		ExamStatusObject.exam_marks=0
		ExamStatusObject.save()
	context={'exam':ExamObject,'status':ExamStatusObject}
	return render(request,'examonline/examguidelines.html',context)

@login_required
@user_is_student
def ExamAttend(request,pk):
	Exam_Object=Exam.objects.get(pk=pk)
	ExamStatusObject=ExamStatus.objects.filter(stud_name=request.user).get(test=Exam_Object)
	if ExamStatusObject.exam_status == True:
		return redirect('/exam/'+str(pk)+'/guidelines')
	questions=Exam_Object.question_set.all()
	ExamObject=Exam.objects.get(pk=pk)
	Estat=ExamStatus.objects.filter(stud_name=request.user).get(test=Exam_Object)
	servertime=Estat.timeleft
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
		browsertime=(request.GET.get('time'))
		if browsertime != None:	
			print("Old Server Time",servertime)
			if(servertime-int(browsertime)<0):
				Estat.timeleft=servertime-2
				Estat.save()	
				print("ERROR BUT UPDATED")
			else:	
				Estat.timeleft=int(browsertime)	
				Estat.save()
				print("REGULAR UPDATION")
			print("Browser Time",int(browsertime))
			print("NewServer Time",Estat.timeleft)
	form=ExamAttendForm()
	form.fields["stud_option"].queryset=Option.objects.filter(question=questions[page_obj.number-1])
	if (Attempted.filter(stud_question=questions[page_obj.number-1])):
		CandidateObject=Candidate.objects.filter(stud_name=request.user).filter(stud_question=questions[page_obj.number-1])
		form=ExamAttendForm(request.POST or None,instance=CandidateObject[0])
		form.fields["stud_option"].queryset=Option.objects.filter(question=questions[page_obj.number-1])
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
			return redirect("/exam/"+str(pk)+"/attend?page="+str(page_obj.next_page_number()))
		else:
			return redirect("/exam/"+str(pk)+"/attend?page="+str(page_obj.previous_page_number()))
	AttemptedQuestions=[]
	for i in q:
		new_obj = paginator.get_page(i)
		if (Attempted.filter(stud_question=questions[new_obj.number-1])):
			AttemptedQuestions.append(i)
	context={'paginator':paginator,'servertime':servertime,'q':q,'AttemptedQuestions':AttemptedQuestions,'page_obj':page_obj,'form':form,}
	return render(request,'examonline/examattend.html',context)

@login_required
@user_is_student
def ExamSubmitView(request,pk):
	ExamObject=Exam.objects.get(pk=pk)
	ExamSubmitObject=ExamStatus.objects.filter(stud_name=request.user).get(test=ExamObject)
	ExamSubmitObject.exam_status=True
	CandidateMarks=Candidate.objects.filter(stud_name=request.user).filter(stud_exam=ExamObject).aggregate(Sum('stud_mark'))
	mark=CandidateMarks.get('stud_mark__sum')
	AnsweredCount=Candidate.objects.filter(stud_name=request.user).filter(stud_exam=ExamObject).count()
	QuestionCount=ExamObject.question_set.all().count()
	UnAnsweredCount=QuestionCount-AnsweredCount
	if (mark):
		pass
	else:
		mark=0
	ExamSubmitObject.exam_marks=mark
	ExamSubmitObject.timeleft=0
	ExamSubmitObject.save()
	students=ExamStatus.objects.filter(test=ExamObject).filter(exam_status=True).order_by('-exam_marks')
	c=students.count()
	for i in students:
		pass
	for i in range(0,c):
		if i == 0:
			students[i].rank=i+1
		elif i!=0 and students[i].exam_marks == students[i-1].exam_marks:
			students[i].rank=students[i-1].rank	
		else:
			students[i].rank=students[i-1].rank+1
		if(students[i].exam_marks >= ExamObject.exam_passmark):
			students[i].save()
		else:
			students[i].rank=-1
			students[i].save()
	context={'result':ExamSubmitObject,'anscount':AnsweredCount,'uanscount':UnAnsweredCount}	
	return render(request,'examonline/result.html',context)

@login_required
@user_is_student
def ExamConfirmSubmit(request,pk):
	context={'pk':pk}
	return render(request,'examonline/confirm.html',context)

@login_required
@user_is_student
def ExamSolutionPaginated(request,pk):
	ExamObject=Exam.objects.get(pk=pk)
	ExamStatusObject=ExamStatus.objects.filter(stud_name=request.user).get(test=ExamObject)
	if ExamStatusObject.exam_status == False:
		raise PermissionDenied
	else:
		questions=ExamObject.question_set.all()
		Attempted=Candidate.objects.filter(stud_name=request.user).filter(stud_exam=ExamObject)
		print(Attempted)
		paginator=Paginator(questions,1)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		print(page_obj.number)
		q=paginator.page_range
		try:
			StudOption=Candidate.objects.filter(stud_name=request.user).get(stud_question=page_obj[0])
		except:
			StudOption=[]
		context={'paginator':paginator,'q':q,'page_obj':page_obj,'questions':questions,'attempted':Attempted,'studoption':StudOption}
		return render(request,'examonline/examsolutionpaginated.html',context)