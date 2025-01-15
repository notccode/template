# certificacion

## Ejecutar el proyecto

- descargar archivo Alvaro_Navarrete_0075.zip
- crear un entorno virtual llamado "sistema"
- activar el entorno virtual y instalar los siguientes modulos: Django y spycopg2

- descomprimir el archivo Alvaro_Navarrete_0075.zip
- entrar a la carpeta Alvaro_Navarrete_0075
- cargar el dump llamado datos.dump en una base de datos postgres llamada "sistema"
- configurar el archivo setting.py del sistema ubicada en certificacion/proyecto/setting.py

``` 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- ejecutar el programa con el siguiente comando python manage.py runserver en certificacion/

## Usuarios por rol





