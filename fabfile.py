"""
This script used to setup new webserver and deploy code.

I use Python + Django + Nginx + Postgres. But you can change
configuration to use MySQL and other packages as you wish.

Before you start, you need to install Fabric with:
    `pip install fabric`

How it works:
- `fab init_server` - prepare new Ubuntu server to be a webserver.
  Uses list of pakages from ubuntu_packages.
- `fab deploy` - deploy new version of Django project to server.
  By the way it copy static files, migrate DB, restart webserver.
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
# list of packages to install on Ubuntu server
ubuntu_packages = (
    'postgresql',
    'python3',
    'nginx',
)


def deploy():
    """
    Deploy project to server and reload nginx.

    Source code updates from a git repository.

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
