from django.core.exceptions import PermissionDenied
from examonline.models import Exam,Question,Option
def user_is_student(function):
	def wrap(request, *args, **kwargs):
		if request.user.is_student == True:
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return wrap

def user_is_teacher(function):
	def wrap(request,*args,**kwargs):
		if request.user.is_teacher==True:
			return function(request,*args,**kwargs)
		else:
			raise PermissionDenied
	return wrap


def user_is_examcreator(function):
	def wrap(request, *args, **kwargs):
		id=kwargs['pk']
		if(Exam.objects.get(pk=kwargs['pk']).exam_creator==request.user):
				return function(request,*args,**kwargs)
		else:
			raise PermissionDenied
	return wrap
def user_is_questioncreator(function):
	def wrap(request, *args, **kwargs):
		id=kwargs['pk']
		if(Question.objects.get(pk=kwargs['pk']).question_creator==request.user):
				return function(request,*args,**kwargs)
		else:
			raise PermissionDenied
	return wrap
def user_is_optioncreator(function):
	def wrap(request, *args, **kwargs):
		id=kwargs['pk']
		if(Option.objects.get(pk=kwargs['pk']).question.question_creator==request.user):
				return function(request,*args,**kwargs)
		else:
			raise PermissionDenied
	return wrap
