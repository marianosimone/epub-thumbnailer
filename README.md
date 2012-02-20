# What?
epub-thumbnailer is a simple script that tries to find a cover into an epub file and creates a thumbnail for it.

# Why?
Because I want nautilus to display nice thumnails for my epub ebooks, as it does for pdf files

# How to install?
Make sure epub-thumbnailer is executable

    chmod +x epub-thumbnailer

Copy epub-thumbnailer to /usr/bin

    sudo cp epub-thumbnailer /usr/bin

Copy epub-thumbnailer.schemas to /usr/share/gconf/schemas/

    sudo cp epub-thumbnailer.schemas /usr/share/gconf/schemas/

Install the schema

    gconftool-2 --install-schema-file /usr/share/gconf/schemas/epub-thumbnailer.schemas

Restart nautilus

    killall -9 nautilus && nautilus

# More info
See http://marianosimone.com.ar/epub-thumbnailer

# Acknowledgments
- [Marcelo Lira](https://github.com/setanta): Improved cover detection by filename
- Pablo Jorge: Added manifest-based cover detection
