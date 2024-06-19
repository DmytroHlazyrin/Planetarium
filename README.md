# Planetarium

### Planetarium API service, built on Django REST, is designed for local planetarium. Provides information about shows, topics, domes, tickets, and reservations.


## Installing

1. Clone the repository:
```shell
git clone https://github.com/DmytroHlazyrin/Planetarium.git
```
2. Go to the project directory:
```shell
cd Planetarium
```
3. Create and activate venv:
```shell
python -m venv venv 
source venv/bin/activate(on macOS)
venv\Scripts\activate(on Windows)
```
4. Set the project assignments:
```shell
pip install -r requirements.txt
```

### Setting up Environment Variables
```shell
touch .env  
```
### Example of environment variables
``` 
 .env.sample 
```

```
set POSTGRES_USER=your db username  
set POSTGRES_PASSWORD= your db password  
set POSTGRES_HOST= your db hostname  
set POSTGRES_DB=your db name  
set PGDATA=setting for docker run  
set SECRET_KEY=your secret key  
```

## Starting the server
1. Create database migrations:
```shell
python manage.py migrate
```
2. Create superuser:
```shell
python manage.py createsuperuser
```

3. Load test data:
```shell
python manage.py loaddata initial_data.json
```

4. Start the development server:
```shell
python manage.py runserver
```

## Start tests
```shell
python manage.py test
```

## Run with Docker
```shell
docker-compose build  
```
```shell
docker-compose up 
```

### Getting access  
```
create user via api/user/register  
```
```
get access token via api/token  
```