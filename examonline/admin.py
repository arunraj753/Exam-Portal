from django.contrib import admin
from examonline.models import Exam,Question,Option,Candidate,ExamStatus
admin.site.register(Exam)
admin.site.register(Option)
admin.site.register(Question)
admin.site.register(Candidate)
admin.site.register(ExamStatus)


