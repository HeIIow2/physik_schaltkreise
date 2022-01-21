# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

import os
import sys
import fileinput

def lineReplace(filename, search, replace, unixEol=False):
    x = fileinput.input(files=filename, inplace=1)
    for line in x:
        line = line.strip('\r\n')
        if search in line:
            line = replace
        print(line)
    x.close()
    if unixEol:
            fileContents = open(filename,"r").read()
            f = open(filename,"w", newline="\n")
            f.write(fileContents)
            f.close()

def verFix(moduleName):
    search = 'site-packages'
    if sys.platform.startswith('linux'):
        search = 'local'
    if sys.platform.startswith('win32'): #if win, use backslash for path
        slash = '\\'
    else:
        slash = '/'
    spackages = next(p for p in sys.path if search in p) #find site-packages forlder
    spackages = spackages+slash+moduleName+slash
    if os.path.isfile(spackages+'VERSION'):
        ver = open(spackages+'VERSION').readline()
        lineReplace(spackages+'__init__.py' , 'VERSION =', 'VERSION = __version__ = "'+ver+'"', True)

# verFix('cairocffi')
# verFix('cairosvg')

block_cipher = None


a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[('C:\\Users\\Lars\\AppData\\Roaming\\Python\\Python39\\site-packages\\cairosvg', 'cairosvg'), ('C:\\Users\\Lars\\AppData\\Roaming\\Python\\Python39\\site-packages\\cairocffi', 'cairocffi')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='gui',
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
