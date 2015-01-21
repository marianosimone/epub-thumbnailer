import argparse
import getopt
import os
import re
import shutil
import sys

from collections import Counter

source_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src')
install_dir = '/usr/bin/'


def copy(src, dst):
    """Copy file <src> to <dst>, creating all necessary dirs in between
    """
    try:
        assert os.path.isfile(src)
        assert not os.path.isdir(dst)
        if not os.path.isdir(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        shutil.copy(src, dst)
        return True
    except Exception:
        return False


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


def gnome_shell_version():
    version = os.popen('gnome-session --version').read().split(' ')
    major_version = version[1][0]
    return ('gnome%s' % major_version) if major_version in set(['2','3']) else None

VERSION_GUSSERS = {
    'mate': lambda: 'gnome3',
    'gnome': gnome_shell_version
}
KNOWN_DE = '|'.join(VERSION_GUSSERS.keys())

def check_gnome_version():
    """
    Checks for the installed gnome version
    returns: 'gnome2' or 'gnome3'
    """
    value = os.popen('ps -A | egrep -i "%s"' % KNOWN_DE).read()  # TODO: What about cinnamon and others?
    counter = Counter(re.findall(r'(%s)' %KNOWN_DE, value))
    if counter:
        desktop_environment = counter.most_common(1)[0][0]
        return VERSION_GUSSERS.get(desktop_environment, lambda: None)()
    return None


def install():
    check_dependencies()
    if not os.access(install_dir, os.W_OK):
        print 'You do not have write permissions to %s (maybe you need to sudo)' % install_dir
        sys.exit(1)

    print 'Installing epub-thumbnailer to %s ...' % install_dir
    if copy(os.path.join(source_dir, 'epub-thumbnailer.py'), os.path.join(install_dir, 'epub-thumbnailer')):
        print 'OK'
        version = check_gnome_version()

        if version == 'gnome2':
            schema = os.path.join(source_dir, 'epub-thumbnailer.schemas')
            os.popen('GCONF_CONFIG_SOURCE=$(gconftool-2 --get-default-source) '
                         'gconftool-2 --makefile-install-rule "%s" 2>/dev/null' %
                            schema)
            print '\nRegistered epub archive thumbnailer in gconf (if available).'
            print 'The thumbnailer is only supported by some file managers, such as Nautilus, Caja and Thunar'
            print 'You might have to restart the file manager for the thumbnaile to be activated.\n'
        elif version == 'gnome3':
            print 'Installing thumbnailer hook in /usr/share/thumbnailers ...'
            if copy(os.path.join(source_dir, 'epub.thumbnailer'), '/usr/share/thumbnailers/epub.thumbnailer'):
                print 'OK'
            else:
                print 'Could not install'
                exit(1)
        else:
            print '\nCould not determine your Gnome version. You can still use the thumbnailer script manually.'
            print ""
            print "For example:"
            print ""
            print "    epub-thumbnailer Lawrence\ Lessig\ -\ Free\ Culture.epub cover.png 128"
            exit(1)
    else:
        print 'Could not install'
        exit(1)

    print 'You might have to restart your file manager for the thumbnailer to be activated.\n'

def uninstall():
    print 'Uninstalling epub-thumbnailer from', install_dir, '...'
    version = check_gnome_version()
    os.remove(os.path.join(install_dir, 'epub-thumbnailer'))
    if version == 'gnome3':
        print 'Uninstalling epub.thumbnailer from /usr/share/thumbnailers/ ...'
        try:
            os.remove('/usr/share/thumbnailers/epub.thumbnailer')
            print 'OK'
        except:
            print("Could not remove /usr/share/thumbnailers/epub.thumbnailer")


commands = {
    'install': install,
    'uninstall': uninstall
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Installs or uninstall epub-thumbnailer on your system')
    parser.add_argument('action', metavar='action', choices=['install', 'uninstall'], help='the action to perform')
    args = parser.parse_args()
    commands[args.action]()
