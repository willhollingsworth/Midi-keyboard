import pynput
import rtmidi
import keyboard


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
    if active_keys:
        if str(key) in active_keys:
            return
    key_event(key, 'down')
    active_keys.append(str(key))


def key_up(key):
    key_event(key, 'up')
    if active_keys:
        if str(key) in active_keys:
            active_keys.remove(str(key))


def key_event(key, state):
    # print(str(key), state)
    if str(key) == 'Key.esc':
        print(key, 'pressed, quiting')
        quit()
    if not 'char' in dir(key):
        return
    if key.char in hotkeys:
        note = starting_note + hotkeys.index(key.char)
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
    midiout.open_port(5)
    return midiout


def disable_regular_hotkey_usage():
    for key in hotkeys:
        keyboard.block_key(key)


global hotkeys
global starting_note
global active_keys

hotkeys = '1234567890qwertyuiopasdfghjklzxcvbnm'
starting_note = 50
active_keys = []

midiout = setup_midi_port()
disable_regular_hotkey_usage()
start_keyboard_listening()
