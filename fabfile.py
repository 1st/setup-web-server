"""
Prepare Django project and upload it to server.

Also this script allows to prepare new Ubuntu server with
list of required packages: install python3, mysql or postgres,
create virtualenv and configure nginx webserver.

I use Fabric to execute commands on the server.
I clone git repository on server and update this repo.
"""
from fabric.api import run, local, hosts, cd, prefix, env
from fabric.contrib import django

# SETTINGS
username = 'username'
# the user to use for the remote commands
env.user = username
# the servers where the commands are executed
env.hosts = ['mydomain.com']
# project settings
project_name = 'myproject'
project_root_dir = '/home/{}/{}'.format(username, project_name)


def deploy():
    """
    Deploy project to server and reload nginx.

    Source code update from a git repository.

    TODO: apply DB migrations.
    """
    with cd(project_root_dir):
        # update source code from git repository
        run('git pull')

        with prefix('source ~/.virtualenvs/{}/bin/activate'.format(project_name)):
            # collect static files
            run('python manage.py collectstatic --noinput')

        # and finally touch the .wsgi file so that mod_wsgi triggers
        # a reload of the application
        run('touch wsgi.py')


def init_server():
    """
    Install system-wide packages and prepare services to work.
    """
    pass


def install_mysql():
    pass


def install_postgres():
    pass


def deploy_code():
    pass


def backup():
    """
    Backup remote server data to local dump.
    """
    backup_database()
    backup_files()


def backup_database():
    pass


def backup_files():
    pass
