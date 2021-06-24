#!/bin/bash

path_to_prog='/home/christopolise/CS_456/playing_around'

dbus-monitor --session "type='signal',interface='org.gnome.ScreenSaver'" |
  while read x; do
    case "$x" in 
      *"boolean true"*) continue;;
      *"boolean false"*) eval $(gnome-terminal --full-screen --window-with-profile=NoScrollbar -- bash -c "gsettings set org.gnome.mutter overlay-key ''; xmodmap -e 'keycode 64='; xmodmap -e 'keycode 108='; source ${path_to_prog}/play_env/bin/activate; python3 ${path_to_prog}/lingo_lock.py; gsettings set org.gnome.mutter overlay-key 'Super_L'; xmodmap -e 'keycode 64=Alt_L'; xmodmap -e 'keycode 108=Alt_R';");;  
    esac
  done

