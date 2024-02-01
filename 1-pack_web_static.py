#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Creates a compressed archive of the web_static folder

    Returns:
        str: Path to the archive if successful, otherwise None
    """
    try:
        # Create the 'versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the archive filename
        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )

        # Compress the contents of the web_static folder
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the archive path
        return "versions/{}".format(archive_name)
    except Exception as e:
        print("Error: {}".format(e))
        return None
