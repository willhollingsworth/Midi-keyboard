from operator import index
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
    global starting_octeve
    if active_keys:
        if str(key) in active_keys:
            return
    key_event(key, 'down')
    if str(key) in utility_hotkeys:
        if str(key) == 'Key.up':
            release_all_held_keys()
            starting_octeve += 1
        if str(key) == 'Key.down':
            release_all_held_keys()
            if starting_octeve > 0:
                starting_octeve -= 1
    active_keys.append(str(key))


def key_up(key):
    key_event(key, 'up')
    if active_keys:
        if str(key) in active_keys:
            active_keys.remove(str(key))


def calc_note_offset(key):
    offset = scale_offset
    scale_target = active_scale
    main_index = note_hotkeys.index(key.char)
    scale_length = len(scale_target)
    scale_index, note_index = divmod(main_index, scale_length)
    if scale_index != 0:
        offset += scale_index*sum(scale_target)
    if note_index != 0:
        offset += sum(scale_target[0:note_index])
    print(main_index, scale_index, note_index, offset)
    return offset


def key_event(key, state):
    print(str(key), state)
    if str(key) == 'Key.esc':
        print(key, 'pressed, quiting')
        release_all_held_keys()
        quit()
    if not 'char' in dir(key):
        return
    if key.char in note_hotkeys:
        note = starting_octeve*8 + calc_note_offset(key)
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
global starting_octeve
global active_keys
global utility_hotkeys

note_hotkeys = '1234567890qwertyuiopasdfghjklzxcvbnm'
utility_hotkeys = ['Key.up', 'Key.down']
# utility_hotkeys = ['Key.' + key for key in utility_hotkeys]
starting_octeve = 0
active_keys = []
major_scale_offsets = [2, 2, 1, 2, 2, 2, 1]
major_scale_root_list = ['c', 'c#', 'd', 'd#',
                         'e', 'e#', 'f',  'g', 'g#',  'a', 'a#', 'b']
root_note = 'a#'
active_scale = major_scale_offsets
scale_offset = major_scale_root_list.index(root_note)
print('scale offset', scale_offset)
midiout = setup_midi_port()
disable_regular_hotkey_usage()
start_keyboard_listening()
