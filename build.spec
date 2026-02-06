# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('dist', 'dist'),
        ('config.json', '.'),
    ],
    hiddenimports=[
        'mido.backends.rtmidi',
        'mido.backends.portmidi',
        'requests',
        'packaging',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='key2midi-pad',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='key2midi-pad',
)

app = BUNDLE(
    coll,
    name='key2midi-pad.app',
    icon=None,
    bundle_identifier='com.key2midi.pad',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSMicrophoneUsageDescription': 'This app needs accessibility access to monitor keyboard input.',
        'NSAppleEventsUsageDescription': 'This app needs accessibility access to monitor keyboard input.',
    },
)
