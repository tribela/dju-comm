from module import Class
from module import TimeTable

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30) # 닉네임
    student_number = models.IntegerFiend() # 학번
    email = models.EmailField() # 이메일
    department = models.CharField(max_length=10) #학부(과)
    grade = models.IntegerField() #학년
    classes = models.ManyToManyField(Class)

    class Meta:
        unique_together = (
            'nickname', 'student_number'
        )

    def __str__(self):
        return 'name'.foramt(
            name=self.name)

