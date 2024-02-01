# Puppet manifest for setting up web_static directory

# Create directory structure
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# Create index.html
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

# Ensure correct ownership and permissions
file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Restart Apache or Nginx or your web server
# This may vary depending on your web server configuration
# For example, for Nginx:
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/data/web_static/current'],
}
