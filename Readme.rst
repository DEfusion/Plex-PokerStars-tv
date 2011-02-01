========
Plex-PokerStars-tv
========

A Plex_ plugin for PokerStars.tv, allowing play of any videos on all of the channels featured on PokerStars.tv website.

Changelog
=========

0.0.2

- new: control videos via the JS API
- new: allow skipping
- new: include progress bar updates
- fix: detection of video completion

0.0.1

- new: initial version
- new: search/browse video clips from pokerstars.tv

Installing
==========
The `Plex-PokerStars.tv`_ plugin release bundle can be downloaded from the `downloads section`_ on github, simple drop in your ``~/Library/Application\ Support/Plex\ Media\ Server/Plug-ins`` directory

Building From Source
====================
The `Plex-PokerStars.tv`_ plugin bundle is built from files in the ``bundle/`` and ``templates/`` directories. To build the bundle you'll need:

* Git_
* Ruby_ & Rake_ (Both are bundled with OS X)

With those tools installed, get a copy of the source and install the plugin::

    $ git clone git://github.com/DEfusion/Plex-PokerStars-tv
    $ cd Plex-PokerStars-tv
    $ rake install

If you'd like to remove the plugin later, use::

    $ rake uninstall

Or, ``rake uninstall:hard`` to get uninstall the plugin *and* it's preferences and data.

Contributing
============
Code contributions are welcome! If you'd like to add a feature, just fork the
project on GitHub and send me a pull request. Be aware that this is the only
thing I've ever written in Python. If you don't know Python well, don't mimic my
style. If you do, go easy on me (and please do refactor!).

After you've forked `Plex-PokerStars-tv`_ on GitHub, install the development version of the bundle::

    $ rake install:development

Plex is now watching ``bundle/`` for changes.  Any edits you make will be automatically loaded by Plex.  Push them up to GitHub and send a pull request.

Links
=====

- Plex_
- `Plex-PokerStars.tv`_ on GitHub
- `Plex-PokerStars.tv's page in the Plex Wiki`_

.. _Plex: http://plexapp.com/
.. _`Plex-PokerStars.tv`: https://github.com/DEfusion/Plex-PokerStars-tv
.. _`Plex-PokerStars.tv's page in the Plex Wiki`: http://wiki.plexapp.com/index.php/MLB
.. _Git: http://code.google.com/p/git-osx-installer/downloads/list?can=3
.. _Ruby: http://www.ruby-lang.org/
.. _Rake: http://rake.rubyforge.org/
.. _`downloads section`: https://github.com/DEfusion/Plex-PokerStars-tv/downloads/