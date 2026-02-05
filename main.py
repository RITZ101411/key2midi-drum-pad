from pynput import keyboard
import mido

outport = mido.open_output('fk2-midi', virtual=True)

KEY_TO_NOTE = {
    'a': 60, 's': 62, 'd': 64, 'f': 65, 'g': 67, 'h': 69, 'j': 71, 'k': 72,
    'w': 61, 'e': 63, 't': 66, 'y': 68, 'u': 70
}

def on_press(key):
    try:
        note = KEY_TO_NOTE.get(key.char)
        if note:
            msg = mido.Message('note_on', note=note, velocity=64)
            outport.send(msg)
            print(f'Sent: {msg}')
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        return False
    try:
        note = KEY_TO_NOTE.get(key.char)
        if note:
            msg = mido.Message('note_off', note=note)
            outport.send(msg)
            print(f'Sent: {msg}')
    except AttributeError:
        pass

def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
