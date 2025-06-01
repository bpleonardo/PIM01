import csv
from collections import defaultdict

from modules.data import get_data_file
from modules.users import User

users = get_data_file('data/logins.json')
courses = get_data_file('data/cursos.json')

course_count = defaultdict(int)
gendered_course_count = defaultdict(lambda: {'h': 0, 'm': 0})
city_count = defaultdict(int)
age_count = defaultdict(int)


def get_range(n):
    if n < 10:
        return (0, 10)
    if n < 20:
        return (10, 20)
    if n < 30:
        return (20, 30)
    if n < 40:
        return (30, 40)
    if n < 50:
        return (40, 50)
    if n < 60:
        return (50, 60)
    if n < 70:
        return (60, 70)
    return (70, 100)


for username in users:
    user = User.find(username)
    assert user is not None
    assert user.course is not None
    assert user.gender is not None

    course_count[user.course.name] += 1
    gendered_course_count[user.course.name][user.gender] += 1
    city_count[user.city] += 1
    age_count[get_range(user.age)] += 1

user_count = len(users)

age_analyis = dict(
    sorted(
        {
            r: (n, n / user_count, n / user_count * 100) for r, n in age_count.items()
        }.items(),
        key=lambda x: x[0][0],
    )
)

city_analysis = dict(
    sorted(
        {
            city: (n, n / user_count, n / user_count * 100)
            for city, n in city_count.items()
        }.items(),
        key=lambda x: x[0],
    )
)

with open('course_stats.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=['Cursos', 'Alunos Matriculados'],
    )
    writer.writeheader()

    for course, count in sorted(course_count.items()):
        writer.writerow({'Cursos': course, 'Alunos Matriculados': count})
    writer.writerow({'Cursos': 'Total de Alunos', 'Alunos Matriculados': user_count})

with open('gendered_course_stats.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=['Cursos', 'Número de Homens', 'Número de Mulheres'],
    )
    writer.writeheader()

    for course, counts in sorted(gendered_course_count.items()):
        writer.writerow(
            {
                'Cursos': course,
                'Número de Homens': counts['h'],
                'Número de Mulheres': counts['m'],
            }
        )

    writer.writerow(
        {
            'Cursos': 'Total',
            'Número de Homens': sum(
                counts['h'] for counts in gendered_course_count.values()
            ),
            'Número de Mulheres': sum(
                counts['m'] for counts in gendered_course_count.values()
            ),
        }
    )
with open('age_stats.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=['Faixa Etária', 'fi', 'fr', 'f%'],
    )
    writer.writeheader()

    for age_range, (count, proportion, percentage) in age_analyis.items():
        writer.writerow(
            {
                'Faixa Etária': f'{age_range[0]} |---------- {age_range[1]}',
                'fi': format(count, '.0f'),
                'fr': format(proportion, '.2f'),
                'f%': format(percentage, '.0f'),
            }
        )
    writer.writerow(
        {
            'Faixa Etária': 'Total',
            'fi': format(user_count, '.0f'),
            'fr': '1.00',
            'f%': '100',
        }
    )

with open('city_stats.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=['Cidade', 'fi', 'fr', 'f%'],
    )
    writer.writeheader()

    for city, (count, proportion, percentage) in city_analysis.items():
        writer.writerow(
            {
                'Cidade': city,
                'fi': format(count, '.0f'),
                'fr': format(proportion, '.2f'),
                'f%': format(percentage, '.0f'),
            }
        )
    writer.writerow(
        {
            'Cidade': 'Total',
            'fi': format(user_count, '.0f'),
            'fr': '1.00',
            'f%': '100',
        }
    )
