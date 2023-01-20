import pytest
import os
from .api import PetFriends
from .settings import valid_password, valid_email

pets = PetFriends()


def test_get_api_key(email=valid_email, password=valid_password):
    # Получаем значеник ключа и статус
    status, result = pets.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets():
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    status, result = pets.get_list_of_pets(auth_key, filter="")
    assert status == 200
    assert result['pets']


def test_add_new_pet():
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    name = "Вася"
    animal_type = "Кенгуру"
    age = "45"
    pet_photo = os.path.join(os.path.dirname(__file__), "images", "cat.jpeg")
    status, result = pets.add_new_pet(auth_key, name, animal_type, age,  pet_photo)
    print(result)
    assert status == 200
    assert result['name'] == name
    assert result ['animal_type'] == animal_type


def test_delete_pet_from_database():
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    _, my_pets = pets.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pets.add_new_pet(auth_key, "Барон -суббота", "кошка", "999", "images/cat.jpg")
        pet_id = my_pets['pets'][0]['id']
        status = pets.delete_pet_from_database(auth_key, pet_id)
        _, my_pets = pets.get_list_of_pets(auth_key, 'my_pets')
        assert status == 200
        assert pet_id not in my_pets.values()


def test_update_information_about_pet():
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    _, my_pets = pets.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    name = "Гаргулия"
    animal_type = "Чебурашка"
    age = "12"
    status, result = pets.update_information_about_pet(auth_key, pet_id, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_post_pet_add_new_pet_without_photo():
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    name = "Виктория"
    animal_type = "Крокодил"
    age = "3"
    status, result = pets.post_pet_add_new_pet_without_photo(auth_key, name, animal_type, age)
    print(result)
    print(auth_key)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type




def test_post_add_photo_of_pet():
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    _, my_pets = pets.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    pet_photo = os.path.join(os.path.dirname(__file__), "images", "kr.jpeg")
    status, result = pets.post_add_photo_of_pet(auth_key, pet_id, pet_photo)
    print(result)
    assert status == 200
    assert result['name']
    assert result['id'] == pet_id
    assert result['pet_photo']

