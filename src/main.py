from pynput import keyboard
import mido
import webview
import os
import json
import time

outport = mido.open_output('fk2-midi', virtual=True)

# Load config
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

KEY_TO_NOTE = {pad['key']: pad['note'] for pad in config['pads']}
KEYS = [pad['key'] for pad in config['pads']]

window = None

# タイミング記録用
key_timings = {}

def calc_velocity(key_down_time, previous_key_down_time, previous_key_up_time):
    # 押下速度（前回KeyUpからの時間差）
    dt_press = key_down_time - previous_key_up_time
    dt_press = max(20, min(dt_press, 200))  # clamp 20〜200ms
    p = 1.0 - (dt_press - 20) / (200 - 20)

    # 連打間隔（前回KeyDownからの時間差）
    dt_repeat = key_down_time - previous_key_down_time
    dt_repeat = max(40, min(dt_repeat, 300))  # clamp 40〜300ms
    r = 1.0 - (dt_repeat - 40) / (300 - 40)

    # ハイブリッド合成（押下速度重視）
    energy = 0.7 * p + 0.3 * r

    # Velocityに変換（40〜127）
    velocity = int(40 + energy * 87)
    return velocity

class Api:
    def pad_press(self, index):
        if index < len(KEYS):
            key = KEYS[index]
            note = KEY_TO_NOTE.get(key)
            if note:
                current_time = time.time() * 1000  # ms
                
                if key not in key_timings:
                    key_timings[key] = {'down': 0, 'up': 0}
                
                prev_down = key_timings[key]['down']
                prev_up = key_timings[key]['up']
                
                if prev_down == 0:
                    velocity = 64
                else:
                    velocity = calc_velocity(current_time, prev_down, prev_up)
                
                key_timings[key]['down'] = current_time
                
                msg = mido.Message('note_on', note=note, velocity=velocity, channel=0)
                outport.send(msg)
                print(f'Sent: {msg}')
                if window:
                    try:
                        window.evaluate_js(f"window.dispatchEvent(new CustomEvent('padPress', {{detail: {{index: {index}, velocity: {velocity}}}}}))")
                    except:
                        pass
    
    def pad_release(self, index):
        if index < len(KEYS):
            key = KEYS[index]
            note = KEY_TO_NOTE.get(key)
            if note:
                current_time = time.time() * 1000  # ms
                key_timings[key]['up'] = current_time
                
                msg = mido.Message('note_off', note=note, velocity=0, channel=0)
                outport.send(msg)
                print(f'Sent: {msg}')
                if window:
                    try:
                        window.evaluate_js(f"window.dispatchEvent(new CustomEvent('padRelease', {{detail: {{index: {index}}}}}))")
                    except:
                        pass

def on_press(key):
    try:
        note = KEY_TO_NOTE.get(key.char)
        if note:
            current_time = time.time() * 1000  # ms
            
            if key.char not in key_timings:
                key_timings[key.char] = {'down': 0, 'up': 0}
            
            prev_down = key_timings[key.char]['down']
            prev_up = key_timings[key.char]['up']
            
            if prev_down == 0:
                velocity = 64
            else:
                velocity = calc_velocity(current_time, prev_down, prev_up)
            
            key_timings[key.char]['down'] = current_time
            
            msg = mido.Message('note_on', note=note, velocity=velocity, channel=0)
            outport.send(msg)
            print(f'Sent: {msg}')
            idx = KEYS.index(key.char)
            if window:
                try:
                    window.evaluate_js(f"window.dispatchEvent(new CustomEvent('padPress', {{detail: {{index: {idx}, velocity: {velocity}}}}}))")
                except:
                    pass
    except (AttributeError, ValueError):
        pass

def on_release(key):
    try:
        note = KEY_TO_NOTE.get(key.char)
        if note:
            current_time = time.time() * 1000  # ms
            key_timings[key.char]['up'] = current_time
            
            msg = mido.Message('note_off', note=note, velocity=0, channel=0)
            outport.send(msg)
            print(f'Sent: {msg}')
            idx = KEYS.index(key.char)
            if window:
                try:
                    window.evaluate_js(f"window.dispatchEvent(new CustomEvent('padRelease', {{detail: {{index: {idx}}}}}))")
                except:
                    pass
    except (AttributeError, ValueError):
        pass

def main():
    global window
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    html_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist', 'index.html'))
    print(f"Loading HTML from: {html_path}")
    window = webview.create_window('fk2-hid-midi', url=f'file://{html_path}', width=500, height=550, resizable=False, js_api=Api())
    webview.start()

if __name__ == "__main__":
    main()
