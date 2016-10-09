from distutils.core import setup
from glob import glob
import py2exe, sys, os
import py2exe
# py2exe.build_exe.py2exe.old_prepare = py2exe.build_exe.py2exe.plat_prepare
data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
sys.argv.append('py2exe')
setup( 
  # data_files=data_files,
  options = {         
    'py2exe' : {
        'compressed': 1, 
        'optimize': 2,
        'bundle_files': 3, #Options 1 & 2 do not work on a 64bit system
        'dist_dir': 'dist',  # Put .exe in dist/
        'xref': False,
        'skip_archive': False,
        'ascii': False,
		'includes': ['lxml.etree', 'lxml._elementpath', 'gzip', 'Tkinter', 'Tkconstants'],
		'excludes': ["tcl", ],
		'dll_excludes': ['tcl85.dll', 'tk85.dll'],
        }
        },                   
  zipfile=None, 
  data_files = [   os.path.join (sys.prefix, "DLLs", f) 
                   for f in os.listdir (os.path.join (sys.prefix, "DLLs")) 
                   if  (   f.lower ().startswith (("tcl", "tk")) 
                       and f.lower ().endswith ((".dll", ))
                       )
                    ] 

    , 
  windows = ['__main__.py'],
)

#def new_prep(self):
#  self.old_prepare()
#  from _tkinter import TK_VERSION, TCL_VERSION
#  self.dlls_in_exedir.append('tcl{0}.dll'.format(TCL_VERSION.replace('.','')))
#  self.dlls_in_exedir.append('tk{0}.dll'.format(TK_VERSION.replace('.','')))
#py2exe.build_exe.py2exe.plat_prepare = new_prep