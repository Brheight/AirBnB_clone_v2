#!/usr/bin/env python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/<archive filename without extension>
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        path_remote = "/data/web_static/releases/{}".format(folder_name)

        run("mkdir -p {}".format(path_remote))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path_remote))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))

        # Move contents to correct folder structure
        run("mv {}/web_static/* {}".format(path_remote, path_remote))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(path_remote))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", str(e))
        return False
