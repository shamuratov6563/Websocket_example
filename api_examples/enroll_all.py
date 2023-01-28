import requests

username = 'jama'
password = '1'

base_url = 'http://127.0.0.1:8000/api/v1/'

# retrieve all courses
try:
    r = requests.get(f'{base_url}courses/')
    courses = r.json()
except requests.exceptions.ConnectionError:
    courses = {}

available_courses = ', '.join([course['title'] for course in courses])
print(f'Available courses : {available_courses}')


for course in courses:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(f'{base_url}courses/{course_id}/enroll/',
                      auth=(username, password))
    # print(r.json()) #it return validation error in second attemp

    if r.status_code == 200:
        # successfull request
        print(f"Successfully enrolled in {course_title}")
    else:
        print(r.json()[0])
