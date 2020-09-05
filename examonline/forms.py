from django import forms
from django.forms import ModelForm
from .models import Exam,Question,Option,Candidate

class ExamCreateForm(forms.ModelForm):
	class Meta:
		model=Exam
		fields=['exam_name','exam_time']
		labels = {
            'exam_time': ('Exam Time (in Minutes)'),
        }

class QuestionCreationForm(forms.ModelForm):
	class Meta:
		model=Question
		#fields='__all__'
		fields=['question','question_mark','question_negative','question_image']

class OptionCreationForm(forms.ModelForm):
	class Meta:
		model=Option
		fields=['option']

class ExamAttendForm(forms.ModelForm):
	stud_option=forms.ModelChoiceField(
		queryset=Option.objects.none(),
		widget=forms.RadioSelect(),
		required=False,	
		empty_label=None,label='Options')
	class Meta:
		model=Candidate
		fields=['stud_option']
class OptionUpdateForm(forms.ModelForm):
	class Meta:
		model=Candidate
		fields=['stud_option']


