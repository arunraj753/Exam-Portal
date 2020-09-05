from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
User=get_user_model()
class Exam(models.Model):
	exam_creator=models.ForeignKey(User,on_delete=models.CASCADE)
	exam_name=models.CharField(max_length=255)
	exam_time=models.IntegerField(default=60)
	exam_marks=models.IntegerField(default=0)
	exam_ready=models.BooleanField(default=False)
	exam_passmark=models.IntegerField(default=1)
	def __str__(self):
		return self.exam_name
class Question(models.Model):
	question_exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
	question=models.CharField(max_length =255,null=True,blank=True)
	question_creator=models.ForeignKey(User,on_delete=models.CASCADE)
	question_description=models.TextField(null=True,blank=True)
	markchoices=[(1,'1'),(2,'2')]
	negativechoices=[
	(0.00, 0.00),(Decimal("0.33"), '0.33'),
	(Decimal("0.66"), '0.66')
	]
	question_mark=models.IntegerField(choices=markchoices, default=1)
	question_negative=models.DecimalField(decimal_places=2, default=0.0, max_digits=3,choices=negativechoices)
	question_image=	models.ImageField(blank=True,null=True,upload_to="images/")
	def __str__(self):
		return ('Question from {}'.format(self.question_exam))
	
class Option(models.Model):
	question=models.ForeignKey(Question,on_delete=models.CASCADE)
	option=models.CharField(max_length=255)
	option_status=models.BooleanField(default=False)
	#option_exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
	def __str__(self):
		return self.option
class Candidate(models.Model):
	stud_name=models.ForeignKey(User,on_delete=models.CASCADE)
	stud_exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
	stud_question=models.ForeignKey(Question,on_delete=models.CASCADE)
	stud_option=models.ForeignKey(Option,on_delete=models.CASCADE)
	stud_mark=models.DecimalField(max_digits=3, decimal_places=2,default=0.00)
	def __str__(self):
		return ('{} by {}'.format(self.stud_question, self.stud_name))
class ExamStatus(models.Model):
	stud_name=models.ForeignKey(User,on_delete=models.CASCADE)
	test=models.ForeignKey(Exam,on_delete=models.CASCADE)
	exam_status=models.BooleanField(default=False)
	exam_marks=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
	rank=models.IntegerField(null=True,blank=True)
	timeleft=models.IntegerField(null=True,blank=True,default=0)
	def __str__(self):
		return ('{} by {} is {} '.format(self.test, self.stud_name,self.exam_status))

