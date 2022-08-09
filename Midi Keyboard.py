import pynput
import rtmidi
import keyboard


def release_all_held_keys():
    # https://github.com/SpotlightKid/python-rtmidi/blob/master/examples/basic/panic.py
    midiout.send_message([0xB0, 0x78, 0])


def send_midi(note, state='up'):
    print('sending midi', state, ', note:', note)
    if state == 'down':
        midi_state = 0x90
        velocity = 127
    elif state == 'up' or True:
        midi_state = 0x80
        velocity = 0
    midiout.send_message([midi_state, note, velocity])


def key_down(key):
    global starting_note
    if active_keys:
        if str(key) in active_keys:
            return
    key_event(key, 'down')
    if str(key) in utility_hotkeys:
        if str(key) == 'Key.up':
            release_all_held_keys()
            starting_note += 1
        if str(key) == 'Key.down':
            release_all_held_keys()
            starting_note -= 1
    active_keys.append(str(key))


def key_up(key):
    key_event(key, 'up')
    if active_keys:
        if str(key) in active_keys:
            active_keys.remove(str(key))


def key_event(key, state):
    print(str(key), state)
    if str(key) == 'Key.esc':
        print(key, 'pressed, quiting')
        release_all_held_keys()
        quit()
    if not 'char' in dir(key):
        return
    if key.char in note_hotkeys:
        note = starting_note + note_hotkeys.index(key.char)
        send_midi(note, state)
    return


def start_keyboard_listening():
    keyboard_listener = pynput.keyboard.Listener(
        on_press=key_down, on_release=key_up)
    keyboard_listener.start()
    keyboard_listener.join()


def setup_midi_port():
    midiout = rtmidi.MidiOut()
    print(rtmidi.MidiOut().get_ports())
    midiout.open_port(4)
    return midiout


def disable_regular_hotkey_usage():
    for key in note_hotkeys:
        keyboard.block_key(key)


global note_hotkeys
global starting_note
global active_keys
global utility_hotkeys

note_hotkeys = '1234567890qwertyuiopasdfghjklzxcvbnm'
utility_hotkeys = ['Key.up', 'Key.down']
# utility_hotkeys = ['Key.' + key for key in utility_hotkeys]
starting_note = 50
active_keys = []
major_scale = [2, 2, 1, 2, 2, 2, 1]

midiout = setup_midi_port()
disable_regular_hotkey_usage()
start_keyboard_listening()
