import pynput
import rtmidi
import keyboard


def release_all_held_keys():
    # https://github.com/SpotlightKid/python-rtmidi/blob/master/examples/basic/panic.py
    midiout.send_message([0xB0, 0x78, 0])


def send_midi(note, state='up'):
    if state == 'down':
        print('sending midi note:', note)
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
    if str(key) in utility_hotkeys:
        utility_functions(str(key))
    else:
        key_event(key, 'down')
    active_keys.append(str(key))


def utility_functions(key):
    global starting_octeve
    global starting_semi
    release_all_held_keys()
    if str(key) == 'Key.up':
        starting_octeve += 1
        print('changing starting octeve', starting_octeve)
    if str(key) == 'Key.down':
        if starting_octeve > 0:
            starting_octeve -= 1
        print('changing starting octeve', starting_octeve)
    if str(key) == 'Key.left':
        starting_semi -= 1
        print('changing starting semi', starting_semi)
    if str(key) == 'Key.right':
        starting_semi += 1
        print('changing starting semi', starting_semi)


def key_up(key):
    key_event(key, 'up')
    if active_keys:
        if str(key) in active_keys:
            active_keys.remove(str(key))


def calc_note_offset(key):
    global starting_octeve
    global starting_semi
    offset = scale_offset
    scale_target = active_scale
    main_index = note_hotkeys.index(key.char) + starting_semi
    scale_length = len(scale_target)+1
    octeve_count, note_index = divmod(main_index, scale_length)
    if octeve_count > 0 or starting_octeve > 0:
        # print(starting_octeve, octeve_count, sum(scale_target))
        offset += (starting_octeve + octeve_count)*sum(scale_target)
    if note_index != 0:
        offset += sum(scale_target[0:note_index])
    # print(main_index, octeve_count, starting_octeve, note_index, offset)
    return offset


def key_event(key, state):
    # print(str(key), state)
    if str(key) == 'Key.esc':
        print(key, 'pressed, quiting')
        release_all_held_keys()
        quit()
    if not 'char' in dir(key):
        return
    if key.char in note_hotkeys:
        note = calc_note_offset(key)
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
global starting_semi
global active_keys
global utility_hotkeys

note_hotkeys = '1234567890qwertyuiopasdfghjklzxcvbnm'
utility_hotkeys = ['Key.up', 'Key.down', 'Key.left', 'Key.right']
# utility_hotkeys = ['Key.' + key for key in utility_hotkeys]
starting_octeve = 0
starting_semi = 0
active_keys = []
major_scale_offsets = [2, 2, 1, 2, 2, 2, 1]
minor_scale_offsets = [2, 1, 2, 2, 1, 2, 2]
root_notes = ['c', 'c#', 'd', 'd#',
                         'e', 'f', 'f#'  'g', 'g#',  'a', 'a#', 'b']

# change the following as required
root_note = 'c'
active_scale = major_scale_offsets

scale_offset = root_notes.index(root_note)
print('scale offset', scale_offset)
midiout = setup_midi_port()
disable_regular_hotkey_usage()
start_keyboard_listening()
