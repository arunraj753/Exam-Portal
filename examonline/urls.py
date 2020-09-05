from django.urls import path
from . import views
urlpatterns=[
path('',views.home,name='home'),
path('home/admin',views.AdminHome,name='home-admin'),

###############  Teacher urls  ############### 
path('home/teacher',views.home_teacher,name='home-teacher'),
path('exam/create',views.ExamCreateView,name='exam-create'),
path('exam/<int:pk>/details',views.ExamDetailsView,name='exam-details'),
path('exam/<int:pk>/edit',views.ExamEditView,name='exam-edit'),
path('exam/<int:pk>/update',views.ExamUpdate,name='exam-update'),
path('exam/<int:pk>/post',views.ExamPost,name='exam-post'),
path('exam/<int:pk>/<int:spk>/solution',views.AnswerPaper,name='stud-solution'),
path('exam/<int:pk>/delete',views.ExamDeleteView,name='exam-delete'),
path('question/create',views.QuestionCreateView,name='question-create'),
path('question/<int:pk>/edit',views.QuestionEditView,name='question-edit'),
path('question/<int:pk>/option/create',views.OptionCreateView,name='option-create'),
path('question/<int:pk>/delete',views.QuestionDeleteView,name='question-delete'),
path('option/<int:pk>/correct',views.TrueOption,name='option-true'),
path('option/<int:pk>/delete',views.OptionDeleteView,name='option-delete'),
path('exam/<int:pk>/rank',views.Rank,name='exam-rank'),
path('exam/<int:pk>/passmark',views.PassMark,name='exam-pass'),
path('exam/<int:pk>/preview',views.ExamPreviewPaginated,name='exam-pag-preview'),

###############  Student urls  ############### 
path('home/student',views.home_student,name='home-student'),
path('exam/<int:pk>/guidelines',views.ExamGuidelinesView,name='exam-guidelines'),
path('exam/<int:pk>/attend',views.ExamAttend,name='exam-attend'),
path('exam/<int:pk>/solution/paginated',views.ExamSolutionPaginated,name='solution-paginated'),
path('exam/<int:pk>/submit',views.ExamSubmitView,name='exam-final-submit'),
path('exam/<int:pk>/confirm',views.ExamConfirmSubmit,name='exam-submit-confirmation'),
]