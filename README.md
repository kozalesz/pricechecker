# PRICE CHECKER
## Instalacja 
1. Stwórz wirtualne środowisko i je aktywuj.
```javascript
virtualenv -p python3 [scieżka instalacji wirtualnego srodowiska]
source [nazwa_katalogu]/bin/activate
```
2. Zainstaluj wymagane biblioteki (plik requirements.txt).
```javascript
install -r requirements.txt
```
3. W folderze skrypty podmieniamy dane do bazy danych w pliku "database_settings.py".
4. W bazie danych tworzymy tabele:
![](http://img.liczniki.org/20191011/Zrzut_ekranu_z_2019_10_11_13_24_40-1570793172.png)
5. Uruchamiamy plik chmielna20.py
6. W katalogu pricechecker tworzymy plik local_settings.py i uzupełniamy go danymi do naszej bazy danych.
```javascript
DATABASES = {
    'default': {
        'NAME': '',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '',
        'USER': '',
        'PASSWORD': '',
    }
}
```
7. Wykonujemy migracje do bazy danych:
```javascript
python3 manage.py migrate
```
8.  Projekt został skonfigurwany!
