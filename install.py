#!/usr/bin/env python

"""
This script installs or uninstalls epub-thumbnailer on your system.
-------------------------------------------------------------------------------
Usage: install.py [OPTIONS] COMMAND

Commands:
    install                  Install epub-thumbnailer

    uninstall                Uninstall epub-thumbnailer
"""

import os
import sys
import getopt
import shutil

source_dir = os.path.dirname(os.path.realpath(__file__))
install_dir = '/usr/bin/'

# Files to be installed, as (source file, destination directory)
FILES = [('epub-thumbnailer', '/usr/bin/')]

def info():
    """Print usage info and exit."""
    print __doc__
    sys.exit(1)

def install(src, dst):
    """Copy <src> to <dst>. The <src> path is relative to the source_dir and
    the <dst> path is a directory relative to the install_dir.
    """
    try:
        dst = os.path.join(install_dir, dst, os.path.basename(src))
        src = os.path.join(source_dir, src)
        assert os.path.isfile(src)
        assert not os.path.isdir(dst)
        if not os.path.isdir(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        shutil.copy(src, dst)
        print 'Installed', dst
    except Exception:
        print 'Could not install', dst

def uninstall(path):
    """Remove the file or directory at <path>, which is relative to the 
    install_dir.
    """
    try:
        path = os.path.join(install_dir, path)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            return
        print 'Removed', path
    except Exception:
        print 'Could not remove', path

def check_dependencies():
    """Check for required and recommended dependencies."""
    required_found = True
    recommended_found = True
    print 'Checking dependencies ...\n'
    print 'Required dependencies:'
    try:
        import Image
        assert Image.VERSION >= '1.1.5'
        print '    Python Imaging Library ....... OK'
    except ImportError:
        print '    !!! Python Imaging Library ... Not found'
        required_found = False
    except AssertionError:
        print '    !!! Python Imaging Library ... version', Image.VERSION,
        print 'found'
        print '    !!! Python Imaging Library 1.1.5 or higher is required'
        required_found = False
    if not required_found:
        print '\nCould not find all required dependencies!'
        print 'Please install them and try again.'
        sys.exit(1)
    print

# ---------------------------------------------------------------------------
# Parse the command line.
# ---------------------------------------------------------------------------
try:
    opts, command = getopt.gnu_getopt(sys.argv[1:], '', [])
except getopt.GetoptError, err:
    print str(err)
    info()

# ---------------------------------------------------------------------------
# Install epub-thumbnailer.
# ---------------------------------------------------------------------------
if command == ['install']:
    check_dependencies()
    print 'Installing epub-thumbnailer to', install_dir, '...\n'
    if not os.access(install_dir, os.W_OK):
        print 'You do not have write permissions to', install_dir
        sys.exit(1)
    for afile in FILES:
        install(afile[0], afile[1])

    schema = os.path.join(source_dir, 'epub-thumbnailer.schemas')
    os.popen('GCONF_CONFIG_SOURCE=$(gconftool-2 --get-default-source) '
                 'gconftool-2 --makefile-install-rule "%s" 2>/dev/null' %
                    schema)
    print '\nRegistered epub archive thumbnailer in gconf (if available).'
    print 'The thumbnailer is only supported by some file managers,',
    print 'such as Nautilus'
    print 'and Thunar.'
    print 'You might have to restart the file manager for the thumbnailer',
    print 'to be activated.'
# ---------------------------------------------------------------------------
# Uninstall epub-thumbnailer.
# ---------------------------------------------------------------------------
elif command == ['uninstall']:
    print 'Uninstalling epub-thumbnailer from', install_dir, '...\n'
    uninstall('epub-thumbnailer')
else:
    info()

