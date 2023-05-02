Список доступных образов
```
C:\>wsl -l -o
The following is a list of valid distributions that can be installed.
Install using 'wsl.exe --install <Distro>'.

NAME                                   FRIENDLY NAME
Ubuntu                                 Ubuntu
Ubuntu-22.04                           Ubuntu 22.04 LTS
...
```

Устанавливаем убунту из образа Ubuntu-22.04 
```
wsl --install -d Ubuntu-22.04
```

Список установленных образов
```
C:\Users\Admin>wsl -l -v
  NAME                   STATE           VERSION
* Ubuntu                 Stopped         2
  Ubuntu-22.04           Running         2
...
```

Удалить можно будет так
```
wsl --unregister Ubuntu-22.04
```

# Логинимся на установленную убунту Ubuntu-22.04
```
wsl ~ -d Ubuntu-22.04
```

