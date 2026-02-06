from pynput import keyboard
import mido
import webview
import os
import json
import sys
import shutil

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    user_config_path = os.path.expanduser('~/Library/Application Support/key2midi-pad/config.json')
    
    if os.path.exists(user_config_path):
        config_path = user_config_path
    else:
        default_config_path = os.path.join(base_path, 'config.json')
        if os.path.exists(default_config_path):
            os.makedirs(os.path.dirname(user_config_path), exist_ok=True)
            shutil.copy(default_config_path, user_config_path)
            config_path = user_config_path
        else:
            config_path = default_config_path
else:
    base_path = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_path, 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

KEY_TO_NOTE = {pad['key']: pad['note'] for pad in config['pads']}
KEYS = [pad['key'] for pad in config['pads']]
VELOCITY = config.get('velocity', 80)

window = None
outport = None
listener = None
window_focused = False
pressed_keys = set()

class Api:
    def set_window_focus(self, focused):
        global window_focused
        window_focused = focused
        return True
    
    def set_always_on_top(self, on_top):
        if window:
            window.on_top = on_top
        return True
    
    def get_config(self):
        return config
    
    def check_updates(self):
        try:
            from src.updater import check_for_updates
            update_info = check_for_updates()
            return update_info
        except Exception as e:
            print(f'Update check error: {e}')
            return None
    
    def download_and_install_update(self, download_url):
        try:
            from src.updater import download_update, open_dmg
            dmg_path = download_update(download_url)
            if dmg_path:
                open_dmg(dmg_path)
                return True
            return False
        except Exception as e:
            print(f'Update install error: {e}')
            return False
    
    def save_config(self, new_config):
        global config, KEY_TO_NOTE, KEYS, VELOCITY
        config = new_config
        KEY_TO_NOTE = {pad['key']: pad['note'] for pad in config['pads']}
        KEYS = [pad['key'] for pad in config['pads']]
        VELOCITY = config.get('velocity', 80)
        
        save_path = config_path
        if getattr(sys, 'frozen', False):
            save_path = os.path.expanduser('~/Library/Application Support/key2midi-pad/config.json')
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    
    def pad_press(self, index):
        if index < len(KEYS):
            key = KEYS[index]
            note = KEY_TO_NOTE.get(key)
            if note and outport:
                try:
                    msg = mido.Message('note_on', note=note, velocity=VELOCITY, channel=0)
                    outport.send(msg)
                except Exception as e:
                    print(f'MIDI send error: {e}')
                if window:
                    try:
                        window.evaluate_js(f"window.dispatchEvent(new CustomEvent('padPress', {{detail: {{index: {index}, velocity: {VELOCITY}}}}}))")
                    except Exception as e:
                        print(f'JS eval error: {e}')
    
    def pad_release(self, index):
        if index < len(KEYS):
            key = KEYS[index]
            note = KEY_TO_NOTE.get(key)
            if note and outport:
                try:
                    msg = mido.Message('note_off', note=note, velocity=0, channel=0)
                    outport.send(msg)
                except Exception as e:
                    print(f'MIDI send error: {e}')
                if window:
                    try:
                        window.evaluate_js(f"window.dispatchEvent(new CustomEvent('padRelease', {{detail: {{index: {index}}}}}))")
                    except Exception as e:
                        print(f'JS eval error: {e}')

def on_press(key):
    if not window_focused:
        return
    try:
        key_char = key.char
        if key_char in pressed_keys:
            return
        
        note = KEY_TO_NOTE.get(key_char)
        if note and outport:
            pressed_keys.add(key_char)
            try:
                msg = mido.Message('note_on', note=note, velocity=VELOCITY, channel=0)
                outport.send(msg)
            except Exception as e:
                print(f'MIDI send error: {e}')
                pressed_keys.discard(key_char)
                return
            idx = KEYS.index(key_char)
            if window:
                try:
                    window.evaluate_js(f"window.dispatchEvent(new CustomEvent('padPress', {{detail: {{index: {idx}, velocity: {VELOCITY}}}}}))")
                except Exception as e:
                    print(f'JS eval error: {e}')
    except (AttributeError, ValueError):
        pass

def on_release(key):
    if not window_focused:
        return
    try:
        key_char = key.char
        note = KEY_TO_NOTE.get(key_char)
        if note and outport:
            pressed_keys.discard(key_char)
            try:
                msg = mido.Message('note_off', note=note, velocity=0, channel=0)
                outport.send(msg)
            except Exception as e:
                print(f'MIDI send error: {e}')
                return
            idx = KEYS.index(key_char)
            if window:
                try:
                    window.evaluate_js(f"window.dispatchEvent(new CustomEvent('padRelease', {{detail: {{index: {idx}}}}}))")
                except Exception as e:
                    print(f'JS eval error: {e}')
    except (AttributeError, ValueError):
        pass

def cleanup():
    global listener, outport
    if listener:
        listener.stop()
    if outport:
        outport.close()

def main():
    global window, outport, listener
    
    try:
        outport = mido.open_output('fk2-midi', virtual=True)
    except Exception as e:
        print(f'Failed to create virtual MIDI device: {e}')
        try:
            outputs = mido.get_output_names()
            if outputs:
                outport = mido.open_output(outputs[0])
            else:
                outport = None
        except Exception as e:
            print(f'Failed to open MIDI device: {e}')
            outport = None
    
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    html_path = os.path.join(base_path, 'dist', 'index.html')
    window = webview.create_window('key2midi-pad', url=f'file://{html_path}', width=500, height=600, resizable=False, js_api=Api())
    
    try:
        webview.start()
    finally:
        cleanup()

if __name__ == "__main__":
    main()
