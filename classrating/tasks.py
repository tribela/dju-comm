import base64
import re
import xlrd

from background_task import background

from .models import Class, Professor, TimeTable


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


@background(schedule=0)
def import_excel(year, semester, xls_content):
    workbook = xlrd.open_workbook(
        file_contents=base64.b64decode(xls_content.encode('ascii')))
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
            year=year,
            semester=semester,
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

        class_.timetables.set(parse_timetables(class_, row[24]))
        class_.save()
