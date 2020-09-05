# Generated by Django 3.0.6 on 2020-09-05 10:13

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=255)),
                ('exam_time', models.IntegerField(default=60)),
                ('exam_marks', models.IntegerField(default=0)),
                ('exam_ready', models.BooleanField(default=False)),
                ('exam_passmark', models.IntegerField(default=1)),
                ('exam_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=255, null=True)),
                ('question_description', models.TextField(blank=True, null=True)),
                ('question_mark', models.IntegerField(choices=[(1, '1'), (2, '2')], default=1)),
                ('question_negative', models.DecimalField(choices=[(0.0, 0.0), (Decimal('0.33'), '0.33'), (Decimal('0.66'), '0.66')], decimal_places=2, default=0.0, max_digits=3)),
                ('question_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('question_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question_exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examonline.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=255)),
                ('option_status', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examonline.Question')),
            ],
        ),
        migrations.CreateModel(
            name='ExamStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_status', models.BooleanField(default=False)),
                ('exam_marks', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('timeleft', models.IntegerField(blank=True, default=0, null=True)),
                ('stud_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examonline.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stud_mark', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('stud_exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examonline.Exam')),
                ('stud_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('stud_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examonline.Option')),
                ('stud_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examonline.Question')),
            ],
        ),
    ]
