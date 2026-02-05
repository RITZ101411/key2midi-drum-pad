from pynput import keyboard
import mido
import tkinter as tk

outport = mido.open_output('fk2-midi', virtual=True)

KEY_TO_NOTE = {
    'a': 60, 's': 62, 'd': 64, 'f': 65, 
    'g': 67, 'h': 69, 'j': 71, 'k': 72,
    'w': 61, 'e': 63, 't': 66, 'y': 68, 
    'u': 70, 'i': 72, 'o': 74, 'p': 76
}

KEYS = ['w', 'e', 't', 'y', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'u', 'i', 'o', 'p']
pads = {}

def on_press(key):
    try:
        note = KEY_TO_NOTE.get(key.char)
        if note:
            msg = mido.Message('note_on', note=note, velocity=64, channel=0)
            outport.send(msg)
            print(f'Sent: {msg}')
            if key.char in pads:
                pads[key.char].config(highlightbackground="#FF0059")
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        return False
    try:
        note = KEY_TO_NOTE.get(key.char)
        if note:
            msg = mido.Message('note_off', note=note, velocity=0, channel=0)
            outport.send(msg)
            print(f'Sent: {msg}')
            if key.char in pads:
                pads[key.char].config(highlightbackground="#c6c6c6")
    except AttributeError:
        pass

def main():
    root = tk.Tk()
    root.title('fk2-hid-midi')
    root.configure(bg='#212121')
    
    for i, key in enumerate(KEYS):
        row, col = divmod(i, 4)
        color = "#dadada"
        label_bg = '#212121'
        
        container = tk.Frame(root, bg="#212121")
        container.grid(row=row, column=col, padx=12.5, pady=2.5)
        
        pad = tk.Frame(container, bg='#1a1a1a', highlightbackground=color, 
                      highlightthickness=2, relief='solid', width=120, height=120)
        pad.pack()
        pad.pack_propagate(False)
        
        label = tk.Label(container, text=f'PAD{i+1}', bg=label_bg, fg=color,
                        font=('Arial', 9), anchor='w')
        label.pack(anchor='w', pady=(4, 0))
        
        pads[key] = pad
    
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()
