from datetime import datetime

from fabric.api import run, env, cd, hosts, settings, execute, local, task,\
    parallel
from fabric.contrib.console import confirm
import os


#env.key_filename = '~/.ssh/id_rsa'
#devserver = 'yorrick@mtlserverolio.dyndns.org:42022'

dbdumps_local_dir = 'dbdump'


@task
def copy_dumps():
    with settings(warn_only=True):
        old_dumpdir = '{0}.old'.format(dbdumps_local_dir)
        output = local('test -d ~/{0}'.format(old_dumpdir))
        if not output.failed:
            local('mv -f ~/{0} .Trash/'.format(old_dumpdir))

        local('scp yorrick@mtlserverolio:/opt/dbdump/ ~')