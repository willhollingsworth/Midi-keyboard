# Midi-keyboard

### Turn a computer keyboard into a music keyboard with midi.

Rebinds all specified keys into midi notes that are sent out to loopmidi.
From there any daw should be able to read those midi note signals.
When run will block all chosen hotkeys normal functions, to quit hit the escape key.

download loopmidi
https://www.tobias-erichsen.de/software/loopmidi.html

## todo

-   add hotkey switching of scales and root note
-   move configs from main file to dedicated config file for easier editing
-   add active app sensing, making it only active in certain programs
-   add overlay to display changes, maybe allow changes via gui or just display hotkeys

original idea from
https://github.com/goldnjohn/KeyMIDI
