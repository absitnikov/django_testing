import pytest
from model_bakery import baker
from rest_framework.test import APIClient


from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.get('/api/v1/courses/1/')
    assert response.status_code == 200
    assert response.data['name'] == courses[0].name


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    assert len(courses) == len(response.data)
    for i, course in enumerate(response.data):
        assert course['id'] == courses[i].id


@pytest.mark.django_db
def test_id_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?id={courses[1].id}')
    assert response.status_code == 200
    assert courses[1].id == response.data[0]['id']


@pytest.mark.django_db
def test_name_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?name={courses[2].name}')
    assert response.status_code == 200
    assert courses[2].name == response.data[0]['name']


@pytest.mark.django_db
def test_course_create(client):
    response = client.post('/api/v1/courses/', data={
        'id': 1,
        'name': 'name'
    })
    assert 201 == response.status_code
    assert response.data['name'] == 'name'


@pytest.mark.django_db
def test_course_update(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.patch(f'/api/v1/courses/{courses[4].pk}/', data={'name': 'name'}, format='json')
    assert 200 == response.status_code
    assert response.data['id'] == courses[4].id
    assert response.data['name'] == 'name'


@pytest.mark.django_db
def test_delete_courses(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 204
    assert courses[0] != Course.objects.filter(id=courses[0].id)


@pytest.mark.django_db
def test_max_students_course(client, student_factory):
    students = student_factory(_quantity=20)
    students_ids = [student.id for student in students]
    response = client.post('/api/v1/courses/',
                           data={'name': 'test_course', 'students': students_ids})
    assert response.status_code == 201






