#!/usr/bin/env python3
"""
Fabric script to automate deployment of web_static content.
"""

from fabric.api import local, env, run, put
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['<IP web-01>', '<IP web-02>']

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        if not os.path.exists('versions'):
            local('mkdir -p versions')

        time_format = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(time_format)
        local('tar -czvf {} web_static'.format(archive_path))

        return archive_path
    except Exception as e:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_folder = '/data/web_static/releases/{}'.format(
            archive_name.split('.')[0]
        )

        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(archive_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, archive_folder))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {}/web_static/* {}'.format(archive_folder, archive_folder))
        run('rm -rf {}/web_static'.format(archive_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(archive_folder))

        print('New version deployed!')
        return True
    except Exception as e:
        return False

def deploy():
    """
    Calls do_pack and do_deploy functions to deploy the web_static content.
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
