# -*- mode: python -*-

block_cipher = None


a = Analysis(['run.py'],
             pathex=['E:\\pyqt5\\py\\moodly\\Moodly'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
             
a.datas+= [('sounds/notify.wav','./sounds/notify.wav' , 'DATA'),
           ('sounds/message.wav','./sounds/message.wav' , 'DATA')]
           
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Moodly',
          debug=False,
          strip=None,
          upx=True,
          icon='moodly.ico',
          console=False )
