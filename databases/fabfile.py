from datetime import datetime

from fabric.api import env, cd, hosts, settings, execute, local, task,\
    parallel, sudo
from fabric.contrib.console import confirm
import os


#env.key_filename = '~/.ssh/id_rsa'
#devserver = 'yorrick@mtlserverolio.dyndns.org:42022'

dbdump_dir = 'dbdump'


@task
def copy():
    with settings(warn_only=True):
        local('mv -f ~/{0}.old .Trash/'.format(dbdump_dir))
        local('mv ~/{0} ~/{0}.old'.format(dbdump_dir))
        local('scp -r yorrick@mtlserverolio:/opt/dbdump/ ~')


@task
def restaure(copy='False'):
    if copy.lower() == 'true':
        copy()

    stop()

    order = ('weekly', 'migration')
    for dir in order:
        output = local('ls ~/{0}/{1}'.format(dbdump_dir, dir))
        print 'output', output
        for dump in output.split():
            print 'dump', dump

    start()


@task
def stop():
    local('sudo -u postgres pg_ctl -D ~/postgres-data/ stop -m immediate')


@task
def start():
    local('sudo -u postgres pg_ctl -D ~/postgres-data/ start')
