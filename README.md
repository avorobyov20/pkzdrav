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
Удалить установленный образ потом можно будет так
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
