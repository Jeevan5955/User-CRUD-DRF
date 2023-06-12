# Geographical-Vector

#### Framework: Django Rest Framework
#### Message Broker: RabbitMQ
#### Worker/Consumer: Celery
#### Database : SQL Lite
#### Reverse Proxy: Nginx
#### WSGI application server : Gunicorn
#### Postman Collection: https://github.com/Jeevan5955/User-CRUD-DRF/blob/main/DRF-CRUD.postman_collection.json

## Validation:

The validation that is used in the Django application is Object-level validation. 

DRF enforces data validation in the deserialization process, which is why you need to call is_valid() before accessing the validated data. If the data is invalid, errors are then appended to the serializer's error property and a ValidationError is thrown.

Only if the data during post or update is valid then it is put in a queue from which celery worker will pickup the task and save it to the database.


Example:


    from rest_framework import serializers
    from examples.models import Movie


    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = '__all__'
            

## Installation:

### Recommendation:

#### Setup virtual environment

### RabbitMQ Installation:

#### `apt-get install -y erlang`

#### `apt-get install rabbitmq-server`

#### `systemctl enable rabbitmq-server`

#### `systemctl start rabbitmq-server`

### How to run :

##### i) `pip install -r requirements.txt`

##### ii) `python manage.py makemigrations`

##### iii) `python manage.py migrate`

##### iv) `python manage.py runserver 8025`

##### v) `Open: http://127.0.0.1:8025/ `

#### Check the status to make sure everything is running smooth:

#### `systemctl status rabbitmq-server`

#### Starting The Worker Process

#### `celery -A accounts worker -l info`


## Database Schema:

![User Scheme](https://github.com/Jeevan5955/User-CRUD-DRF/assets/54932235/babc3426-703c-4780-8cc5-80ccbcb30bba)


## Deployment :

### i) WSGI application server - Gunicorn:

Gunicorn is a WSGI server

Gunicorn is built so many different web servers can interact with it. It also does not really care what you used to build your web application - as long as it can be interacted with using the WSGI interface.

Gunicorn takes care of everything which happens in-between the web server and your web application. This way, when coding up your a Django application you don’t need to find your own solutions for:

   a) communicating with multiple web servers
   
   b) reacting to lots of web requests at once and distributing the load
   
   c) keeping multiple processes of the web application running
   
#### Configuration of Gunicorn

Create and open a systemd service file for Gunicorn with sudo privileges in your preferred text editor. The service filename should match the socket filename with the exception of the extension:

`sudo nano /etc/systemd/system/webapp.service`

Add the below code and change the respective like service name,path of application and path of gunicorn

Path of application : `pwd`

Path of gunicorn : `which gunicorn`

    [Unit]
    Description=webapp daemon
    After=network.target

    [Service]
    PIDFile=/var/run/webapp.pid
    WorkingDirectory={path of Django application}
    ExecStart={path of gunicorn} --config {path of Django application}/webapp.py --pid /var/run/webapp.pid account.wsgi:application
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s TERM $MAINPID
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

Reload the daemon to reread the service definition:

    sudo systemctl daemon-reload
    
Then restart the Gunicorn process:

    sudo systemctl restart webapp
    
Similary for webapp1 and webapp2

##### Deploying Celery in production:

Create celery environment file:

    sudo nano /etc/default/accountceleryd
    
Add the below code and add the path of celery:

Path of celery: `which celery`

    CELERYD_NODES="worker1 worker2"

    # The name of the Celery App, should be the same as the python file
    # where the Celery tasks are defined
    CELERY_APP="accounts"

    # Log and PID directories
    CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
    CELERYD_PID_FILE="/var/run/celery/%n.pid"

    # Log level
    CELERYD_LOG_LEVEL=INFO

    # Path to celery binary, that is in your virtual environment
    CELERY_BIN={Path of celery}
    
Creating celery as service:
 
    sudo nano /etc/systemd/system/accountworker.service
    
Add the below code and add the path of working directory:

    [Unit]
    Description=Celery Service
    After=network.target

    [Service]
    Type=forking
    User=root
    EnvironmentFile=/etc/default/accountceleryd
    WorkingDirectory={path of working directory}
    ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
      -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
      --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
    ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
      --pidfile=${CELERYD_PID_FILE}'
    ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
      -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
      --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

    [Install]
    WantedBy=multi-user.target
    
Reload the daemon to reread the service definition:

    sudo systemctl daemon-reload
    
Then restart the Gunicorn process of celery worker:

    sudo systemctl restart accountworker


#### ii) Configure Nginx to Proxy Pass: 

Now that Gunicorn is set up, next you’ll configure Nginx to pass traffic to the process.

Installation:

    sudo apt install nginx

Start by creating and opening a new server block in Nginx’s sites-available directory:

    sudo nano /etc/nginx/sites-available/accounts

Add the below code and change the repective domain name: 

    upstream accounts {
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
    }

    server {
            listen 80;
            server_name www.domain.com ;
            proxy_set_header Access-Control-Allow-Origin *;

            location / {
                proxy_pass http://accounts;
                proxy_set_header "Access-Control-Allow-Origin" *;
                proxy_set_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS, HEAD, DELETE";
                proxy_set_header "Access-Control-Allow-Headers" "Authorization, Origin, X-Requested-With, Content-Type, Accept";
                proxy_set_header   X-Real-IP $remote_addr;
                proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header   X-Forwarded-Host $server_name;
                #proxy_set_header   X-Forwarded-Proto https;
            }
    }
    
Next, create a symlink of this Nginx configuration in the sites-enabled folder by running the following command: 
 
    sudo ln -s /etc/nginx/sites-available/accounts /etc/nginx/sites-enabled
 
Testing the configuration file: 

    sudo nginx -t 
    
Next, reload your Nginx configurations by running the reload command: 

    sudo service nginx reload
    
Load Balancing Algorithm:

Round Robin – Requests are distributed evenly across the servers, with server weights taken into consideration. This method is used by default.
    
 #### iii) HTTP to HTTPS using Certbot:
 
     sudo apt-get install python3-certbot-nginx 
     sudo certbot --nginx


Nginx Deployment Documentation: [Nginx deployment documentation.pdf](https://github.com/Jeevan5955/Geographical-Vector/files/8459463/Nginx.deployment.documentation.pdf)


## Complete production architecture:

![User Flow Diagram](https://github.com/Jeevan5955/User-CRUD-DRF/assets/54932235/4529bc4e-6eac-4c93-818a-f92b8db8fb1c)

#### Reference: 

i) https://www.designmycodes.com/python/use-celery-with-django.html

ii) https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

iii) https://www.nginx.com/resources/wiki/start/topics/examples/loadbalanceexample/



