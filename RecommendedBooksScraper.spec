# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['RecommendedBooksScraper.py'],
             pathex=['C:\\UserData\\z003x99j\\Documents\\Code projects\\Personal\\Goodreads WebScraper'],
             binaries=[],
             datas=[],
             hiddenimports=['requests'],
             hookspath=['.'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='RecommendedBooksScraper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
