# Installation

## Python package
```
pip install -r requirements.txt
```

## local sqlite db
```
python manage.py db init
python manage.py db migrate -m "Init db"
python manage.py db upgrade
```

# Run

## Test
```
python manage.py test
```

## Run server
```
python manage.py run
```
