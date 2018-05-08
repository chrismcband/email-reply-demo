Install
=========


Designed to run on ubuntu 16.04.

You will need to install python 3.6, to do that::

    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.6 python3.6-dev


Install system dependencies by running this from the project directory::

    utility/install_os_dependencies.sh


Install python packages once you have created a virtual environment, specifying python 3.6::

    mkvirtualenv --python=/usr/bin/python3.6
    utility/install_python_dependencies.sh


Create a postgres database and user::

    createdb -E UTF8 -T template0 --locale=en_US.utf8 email_reply_demo
    createuser -P emaildemo
    psql
    GRANT ALL PRIVILEGES ON DATABASE "email_reply_demo" TO "emaildemo";


Set up a local .env file containing your environment variables
Export an environment variable so that subsequent commands will use your .env file::

    export DJANGO_READ_DOT_ENV_FILE=on

Run migrations::
    ./manage.py migrate


Create superuser::
    ./manage.py createsuperuser


Start local dev server::
    ./manage.py runserver 0.0.0.0:8000