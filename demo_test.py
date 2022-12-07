import pytest


class People:
    def __init__(self, name, age):
        self.age = age
        self.name = name

    def set_age(self, new_age):
        if type(new_age) == int:
            self.age = new_age
            return
        raise ValueError

    def __str__(self):
        return f"People {self.age} возраст {self.age}"

@pytest.fixture
def people():
    people = People("Иван", 32)
    return people

def test_create_people(people):
    """
    Проверяем создание Человека
    """
    assert people.name == "Иван"
    assert people.age == 32

def test_set_age(people):
    assert people.age == 32
    people.set_age(50)
    assert people.age == 50

def test_set_age_uncorrect(people):
    assert people.age == 32
    with pytest.raises(ValueError):
        people.set_age(2.5)
    assert people.age == 32