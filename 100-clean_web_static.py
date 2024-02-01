#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py) that
deletes out-of-date archives using the function do_clean.
"""

from fabric.api import env, run, local, lcd
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_pack():
    """Create a tar archive of the web_static folder."""
    try:
        local("mkdir -p versions")
        archive_name = "web_static_{}.tgz".format(
            datetime.now().strftime("%Y%m%d%H%M%S"))
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Deploy the web_static content to the web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_no_ext = archive_name.split(".")[0]
        release_path = "/data/web_static/releases/{}".format(archive_no_ext)

        # Upload the archive
        put(archive_path, "/tmp/{}".format(archive_name))

        # Create the release directory
        run("mkdir -p {}".format(release_path))

        # Extract the archive
        run("tar -xzf /tmp/{} -C {}".format(archive_name, release_path))

        # Move the content to the final destination
        run("mv {}/web_static/* {}".format(release_path, release_path))

        # Remove the symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")

        return True
    except Exception as e:
        return False


def do_clean(number=0):
    """Delete out-of-date archives."""
    try:
        number = int(number)
        if number < 0:
            number = 0

        with lcd("versions"):
            local("ls -1t | tail -n +{} | xargs rm -f".format(number + 1))

        releases_path = "/data/web_static/releases"
        run("ls -1t {}/ | tail -n +{} | xargs -I {{}} rm -rf {}/{{}}".format(
            releases_path, number + 1, releases_path))
        print("Cleaned up!")
    except Exception as e:
        print(e)
