import re
import xlrd

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


class DataFile(models.Model):

    year = models.PositiveIntegerField(default=0)
    semester = models.CharField(max_length=4, choices=(
        ('1', '1'),
        ('2', '2'),
        ('1e', '여름'),
        ('2e', '겨울'),
    ), default='1')
    data = models.FileField()

    @staticmethod
    def parse_timetables(class_, rawstring):
        pattern = re.compile(
            r'(?!, )((?P<place>.+?):)?'
            r'(?P<day>[월화수목금토일])\((?P<times>\d+(?:,\d+)*)\)')
        day_map = {
            '월': '1',
            '화': '2',
            '수': '3',
            '목': '4',
            '금': '5',
            '토': '6',
            '일': '7',
        }
        timetables = []
        for item in pattern.finditer(rawstring):
            if item.group('place'):
                place = item.group('place').strip()
            day = item.group('day')
            times = item.group('times')
            for time in map(int, times.split(',')):
                timetable, created = TimeTable.objects.get_or_create(
                    class_to=class_,
                    day=day_map[day],
                    time=time)
                timetable.place = place
                if created:
                    timetable.save()
                timetables.append(timetable)

        return timetables

    def save(self, *args, **kwargs):

        content = self.data.read()
        workbook = xlrd.open_workbook(file_contents=content)
        sheet = workbook.sheet_by_index(0)
        for i in range(2, sheet.nrows):
            row = sheet.row_values(i)

            professor_name = row[5]
            professor_depart = row[6]
            professor, created = Professor.objects.get_or_create(
                name=professor_name, depart=professor_depart)
            if created:
                professor.save()

            code = row[1]
            division = row[3]
            title = row[2]
            classification = row[4]
            try:
                capacity = int(row[7])
            except ValueError:
                capacity = 0
            university = row[10]
            department = row[11]
            major = row[12]
            category = row[13]
            try:
                grade = int(row[14])
            except ValueError:
                grade = None
            try:
                credit = int(row[16])
            except ValueError:
                credit = 0

            class_, created = Class.objects.update_or_create(
                year=self.year,
                semester=self.semester,
                code=code,
                division=division,
                defaults={
                    'title': title,
                    'professor': professor,
                    'classification': classification,
                    'capacity': capacity,
                    'university': university,
                    'department': department,
                    'major': major,
                    'category': category,
                    'grade': grade,
                    'credit': credit,
                })

            class_.timetables.set(DataFile.parse_timetables(class_, row[24]))
            class_.save()
