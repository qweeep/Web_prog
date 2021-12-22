import requests


print('Создание пользователя:')
response = requests.put(
    'http://10.0.0.193:8080/user/boca',
    {'password': 'fsdv4w5#'}
)
print(response.json())

print('Создание пользователя с таким же паролем:')
response = requests.put(
    'http://10.0.0.193:8080/user/joca',
    {'password': 'fsdv4w5#'}
)
print(response.json())

print('Попытка создать пользователя с уже существующим именем:')
response = requests.put(
    'http://10.0.0.193:8080/user/boca',
    {'password': '3456oijUYr'}
)
print(response.json())

print('Получение данных о пользователе:')
response = requests.get('http://10.0.0.193:8080/user/boca')
print(response.json())

print('Удаление пользователя:')
response = requests.delete('http://10.0.0.193:8080/user/joca')
print(response.text)

print('Попытка получить информацию о несуществующем пользователе:')
response = requests.get('http://10.0.0.193:8080/user/joca')
print(response.json())
