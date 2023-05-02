## Инструкции по развертыванию приложения на WSL

### Получить список доступных образов
```
C:\>wsl -l -o
The following is a list of valid distributions that can be installed.
Install using 'wsl.exe --install <Distro>'.

NAME                                   FRIENDLY NAME
Ubuntu                                 Ubuntu
Ubuntu-22.04                           Ubuntu 22.04 LTS
...
```
### Установить ubuntu из образа Ubuntu-22.04 
```
wsl --install -d Ubuntu-22.04
```
### Получить список установленных образов
```
C:\Users\Admin>wsl -l -v
  NAME                   STATE           VERSION
* Ubuntu                 Stopped         2
  Ubuntu-22.04           Running         2
...
```
### ... удалить установленный образ потом можно будет так
```
wsl --unregister Ubuntu-22.04
```
### Залогиниться
```
wsl ~ -d Ubuntu-22.04
```

### Выполнить команды
```
sudo apt update
sudo apt install python3.10-venv
git clone https://github.com/avorobyov20/pkzdrav.git
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






