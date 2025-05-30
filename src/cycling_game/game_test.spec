# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules
from pathlib import Path
import os


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        (str(Path("src/cycling_game/Resources").resolve()), "Resources"),
        (str(Path("src/cycling_game/Resources/Images").resolve()), "Resources/Images"),
        (str(Path("src/cycling_game/Resources/Font").resolve()), "Resources/Font"),
        (str(Path("src/cycling_game/Resources/Sounds").resolve()), "Resources/Sounds"),
        (str(Path("src/cycling_game/Resources/Images/Blood").resolve()), "Resources/Images/Blood"),
        (str(Path("src/cycling_game/Resources/Images/Player").resolve()), "Resources/Images/Player"),
        (str(Path("src/cycling_game/Resources/Images/Local").resolve()), "Resources/Images/Local"),
        (str(Path("src/cycling_game/Resources/Images/Explosion").resolve()), "Resources/Images/Explosion"),
        (str(Path("src/cycling_game/Resources/Images/Tourist").resolve()), "Resources/Images/Tourist"),
        (str(Path("src/cycling_game/highscore.txt").resolve()), ".")
    ],

    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Tourist Bowling',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='Tourist Bowling.app',
    icon="Resources/Images/icon.icns",
    bundle_identifier=None,
)
