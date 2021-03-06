minecraft-ctl
=============

This is a little wrapper for the minecraft server that makes it possible to
send commands to a minecraft server from the command line. This is useful in
particular to automatically and safely create world backups by sending the
save-off command before creating the backup and save-on after the backup is
finished.


instructions
------------

1. Copy ctloptions.py somewhere (possibly into your minecraft server folder) and
   edit it as necessary. If it is not in your minecraft server folder be sure to
   set change the 'dir' setting to point to it. ::

       cp ctloptions.py /somewhere/minecraft/

2. Run minecraft with the folder where options.py is located as first
   argument. (or run it from that folder without arguments). ::

       minecraft /somewhere/minecraft/

   Alternativly copy the initscript to /etc/init.d, edit it to the correct paths
   and start it. Only tested on Debian. ::

       cp initscript /etc/init.d/minecraft
       vim /etc/init.d/minecraft # fix paths
       update-rc.d minecraft defaults
       /etc/init.d/minecraft start

3. Send commands to the server using "minecraft-ctl [<socket>] <command>". The
   control socket defaults to /tmp/minecraft-ctl if left out. ::

       minecraft-ctl say hello

   or ::

       minecraft-ctl /tmp/minecraft-ctl-2 say hello


special commands
----------------

In addition to the regular minecraft server commands the following special
commands are interpreted by the wrapper and not passed through to the server:

``ctl-log <message>``
   Write a message to the minecraft-ctl logfile (ctl.log in the minecraft
   folder by default)

``stop``
   This command is passed through to the server, but specialcased in the
   wrapper to prevent automatic restarting when the server exits.
