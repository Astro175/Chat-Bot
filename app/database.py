import os

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'mysqlachemy',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')
