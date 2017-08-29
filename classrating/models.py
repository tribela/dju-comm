from django.db import models


class Professor(models.Model):
    name = models.CharField(max_length=30)
    depart = models.CharField(max_length=30)

    def __str__(self):
        return '{} - {}'.format(self.name, self.depart)


class Class(models.Model):
    # TODO: db_index=True
    year = models.PositiveIntegerField(default=None)
    semester = models.CharField(max_length=4, choices=(
        ('1', '1'),
        ('2', '2'),
        ('1e', '여름'),
        ('2e', '겨울'),
    ), default='1')
    code = models.CharField(max_length=6)  # 학수번호
    division = models.CharField(max_length=5)  # 분반
    title = models.CharField(max_length=100)  # 과목명
    classification = models.CharField(max_length=10)  # 이수구분
    professor = models.ForeignKey(Professor, related_name='classes', null=True)
    capacity = models.IntegerField()  # 수강제한인원
    university = models.CharField(max_length=40)  # 대학
    department = models.CharField(max_length=40)  # 학부(과)
    major = models.CharField(max_length=40)  # 학과(전공)
    category = models.CharField(max_length=40)  # 과정구분
    grade = models.IntegerField(null=True)  # 학년
    credit = models.IntegerField()  # 학점

    class Meta:
        unique_together = (
            'year', 'semester', 'code', 'division'
        )

    def __str__(self):
        return '{title} - {division}'.format(
            title=self.title, division=self.division)


class TimeTable(models.Model):
    class_to = models.ForeignKey(Class, related_name='timetables')
    day = models.CharField(max_length=1, choices=(
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    ), default='7')  # 7 Should not be used.
    time = models.PositiveIntegerField(default=0)
    place = models.CharField(max_length=30)

    class Meta:
        unique_together = ('class_to', 'day', 'time')

    def __str__(self):
        return '{} - {} {}'.format(
            self.place, self.day, self.time
        )
