# What?
epub-thumbnailer is a simple script that tries to find a cover into an epub file and creates a thumbnail for it.

# Why?
Because I want my file manager (Nautilus, Thunar, Caja, et al.) to display nice thumnails for my epub ebooks, as it does for pdf files or images

# How to install?

Run the installer!

    sudo python install.py install

Basically, it moves the thumbnailer script to /usr/bin and installs the necessary hooks:

- In gnome2, using a gconf schema (check src/epub-thumbnailer.schemas)
- In gnome3, using a thumbnailer entry (check src/epub.thumbnailer)

After installation, you might need to restart your file manager and remove cached thumbnails (~/.cache/thumbnails)

# Acknowledgments
- [Marcelo Lira](https://github.com/setanta): Improved cover detection by filename
- [Pablo Jorge](https://github.com/pablojorge): Added manifest-based cover detection
- [Renato Ramonda](https://github.com/renatoram): Added gnome3 thumbnailer support
