import argparse
import os
import re
import shutil
import sys

from collections import Counter

source_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src')
install_dir = '/usr/bin/'


def copy(src, dst):
    """Copy file <src> to <dst>, creating all necessary dirs in between"""
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
    """Check for required dependencies."""
    required_found = True
    print('Checking dependencies ...\n')
    print('Required dependencies:')

    print('    Python Imaging Library .......')
    try:
        from PIL import Image
        print('OK')
    except ImportError:
        required_found = False
        try:
            import Image
            assert Image.VERSION >= '1.1.5'
            required_found = True
        except AssertionError:
            print('    !!! version ' + Image.VERSION + ' found, but 1.1.5 or higher is required')
            required_found = False
        except ImportError:
            pass
        finally:
            if not required_found:
                print('    ... Not found')
    if not required_found:
        print('\nCould not find all required dependencies!')
        print('Please install them and try again.')
        sys.exit(1)
    print('')

MAJOR_VERSION_EXTRACTOR = re.compile(r'.* (\d*)\..*')
def gnome_shell_version():
    major_version = None
    gnome_session_match = MAJOR_VERSION_EXTRACTOR.search(os.popen('gnome-session --version').read())  # output is "gnome-session X.Y.Z"
    major_version = gnome_session_match and gnome_session_match.group(1)
    if not major_version:
        gnome_shell_match = MAJOR_VERSION_EXTRACTOR.search(os.popen('gnome-shell --version').read())  # output is "GNOME Shell X.Y.Z"
        major_version = gnome_shell_match and gnome_shell_match.group(1)
    return ('gnome%s' % major_version) if major_version in set(['2', '3']) else None

VERSION_GUSSERS = {
    'mate': lambda: 'gnome3',
    'gnome': gnome_shell_version,
    'xfce4': lambda: 'xfce4',
    'unity': lambda: 'unity'
}
KNOWN_DE = '|'.join(VERSION_GUSSERS.keys())

def check_desktop_env():
    """
    Checks for the installed gnome version
    returns: 'gnome2', 'gnome3' or 'xfce4'
    """
    value = os.popen('ps -A | egrep -i "%s"' % KNOWN_DE).read()  # TODO: What about cinnamon and others?
    counter = Counter(re.findall(r'(%s)' % KNOWN_DE, value))
    if counter:
        desktop_environment = counter.most_common(1)[0][0]
        return VERSION_GUSSERS.get(desktop_environment, lambda: None)()
    return None


def install():
    check_dependencies()
    if not os.access(install_dir, os.W_OK):
        print('You do not have write permissions to %s (maybe you need to sudo)' % install_dir)
        sys.exit(1)

    print('Installing epub-thumbnailer to %s ...' % install_dir)
    if copy(os.path.join(source_dir, 'epub-thumbnailer.py'), os.path.join(install_dir, 'epub-thumbnailer')):
        print('OK')
        environment = check_desktop_env()

        if environment == 'gnome2':
            schema = os.path.join(source_dir, 'epub-thumbnailer.schemas')
            os.popen('GCONF_CONFIG_SOURCE=$(gconftool-2 --get-default-source) '
                         'gconftool-2 --makefile-install-rule "%s" 2>/dev/null' %
                            schema)
            print('\nRegistered epub archive thumbnailer in gconf (if available).')
            print('The thumbnailer is only supported by some file managers, such as Nautilus, Caja and Thunar')
            print('You might have to restart the file manager for the thumbnailer to be activated.\n')
        elif environment in ('gnome3', 'xfce4', 'unity'):
            print('Installing thumbnailer hook in /usr/share/thumbnailers ...')
            if copy(os.path.join(source_dir, 'epub.thumbnailer'), '/usr/share/thumbnailers/epub.thumbnailer'):
                print('OK')
            else:
                print('Could not install')
                exit(1)
        else:
            print('\nCould not determine your desktop environment version. You can still use the thumbnailer script manually.')
            print('')
            print('For example:')
            print('')
            print('    epub-thumbnailer Lawrence\ Lessig\ -\ Free\ Culture.epub cover.png 128')
            exit(1)
    else:
        print('Could not install')
        exit(1)

    print('You might have to restart your file manager for the thumbnailer to be activated.\n')

def uninstall():
    print('Uninstalling epub-thumbnailer from', install_dir, '...')
    environment = check_desktop_env()
    os.remove(os.path.join(install_dir, 'epub-thumbnailer'))
    if environment in ('gnome3', 'xfce4', 'unity'):
        print('Uninstalling epub.thumbnailer from /usr/share/thumbnailers/ ...')
        try:
            os.remove('/usr/share/thumbnailers/epub.thumbnailer')
            print('OK')
        except:
            print('Could not remove /usr/share/thumbnailers/epub.thumbnailer')


commands = {
    'install': install,
    'uninstall': uninstall
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Installs or uninstall epub-thumbnailer on your system')
    parser.add_argument('action', metavar='action', choices=['install', 'uninstall'], help='the action to perform')
    args = parser.parse_args()
    commands[args.action]()
