# Выполненное тестовое задание в компанию КОМТЕК
Описание задачи см. в файле ```python-task.pdf```

## Инструкции по развертыванию на WSL

### Получить список доступных образов
```
C:\>wsl -l -o
NAME                                   FRIENDLY NAME
Ubuntu                                 Ubuntu
Ubuntu-22.04                           Ubuntu 22.04 LTS
...
```
### Установить ubuntu из образа Ubuntu-22.04 
```
C:\>wsl --install -d Ubuntu-22.04
```
### Получить список установленных образов
```
C:\>wsl -l -v
  NAME                   STATE           VERSION
* Ubuntu                 Stopped         2
  Ubuntu-22.04           Running         2
...
```
### ... удалить установленный образ потом можно будет так
```
C:\>wsl --unregister Ubuntu-22.04
```
### Залогиниться
```
C:\>wsl ~ -d Ubuntu-22.04
```

### Выполнить команды
```
sudo apt update
sudo apt install python3.10-venv
git clone https://github.com/artemgv/pkzdrav.git
cd pkzdrav
python3 -m venv env
. env/bin/activate
python -m pip install --upgrade pip
```

### Установить библиотеки
#### ... по файлу requirements.txt
```
pip install -r requirements.txt
```
#### ... либо вручную, если нужны последние версии
```
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install drf-yasg
pip install requests
pip install pytest
pip freeze > requirements.txt
```

### Подготовить приложение к запуску
```
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'secret')"
python manage.py 01_gen_test_data
python manage.py 02_gen_files_with_reference_data_for_pytest
```

### Запустить приложение
```
python manage.py runserver
```

### Войти в административную панель
```
http://127.0.0.1:8000/admin
user: admin
password: secret
```

### Ознакомиться с документацией на API
```
http://127.0.0.1:8000/swagger
http://127.0.0.1:8000/redoc
```

### Не завершая работу веб-сервера, открыть параллельно второй сеанс с Ubuntu-22.04
```
C:\>wsl ~ -d Ubuntu-22.04
```
### ... и запустить в нем тесты
```
cd pkzdrav
. env/bin/activate
pytest api/tests/01_data_driven_tests.py
```
