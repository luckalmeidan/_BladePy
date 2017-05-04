# -*- mode: python -*-
import subprocess

try:
	version = subprocess.check_output(["git", "describe", "--abbrev=4", "--always", "--tags"])
	version = version.decode('utf-8').replace('\n', '')

except:
	version = "git_versionless"

with open("../bladepy/VERSION.txt", 'w') as version_file:
	version_file.write(version)

block_cipher = None

a = Analysis(['../bladepy_run.py'],
             pathex=['.'],
             binaries=[],
             datas=[('../bladepy/', './bladepy')],
             hiddenimports=[
			 
			'OCC._AIS',
			'OCC._Aspect',
			'OCC._Bnd',
			'OCC._BRep',
			'OCC._BRepBuilderAPI',
			'OCC._BRepPrim',
			'OCC._BRepPrimAPI',
			'OCC._BRepSweep',
			'OCC._BRepTools',
			'OCC._Dico',
			'OCC._DsgPrs',
			'OCC._Geom',
			'OCC._Geom2d',
			'OCC._GeomAbs',
			'OCC._gp',
			'OCC._Graphic3d',
			'OCC._HLRAlgo',
			'OCC._IFSelect',
			'OCC._IGESCAFControl',
			'OCC._IGESControl',
			'OCC._Image',
			'OCC._Interface',
			'OCC._Message',
			'OCC._MMgt',
			'OCC._NCollection',
			'OCC._OSD',
			'OCC._Poly',
			'OCC._Prs3d',
			'OCC._PrsMgr',
			'OCC._Quantity',
			'OCC._Resource',
			'OCC._Select3D',
			'OCC._SelectBasics',
			'OCC._SelectMgr',
			'OCC._Standard',
			'OCC._StdSelect',
			'OCC._Sweep',
			'OCC._TColgp',
			'OCC._TCollection',
			'OCC._TColStd',
			'OCC._TDataStd',
			'OCC._TDF',
			'OCC._TDocStd',
			'OCC._TopAbs',
			'OCC._TopLoc',
			'OCC._TopoDS',
			'OCC._TopTools',
			'OCC._TShort',
			'OCC._V3d',
			'OCC._Visual3d',
			'OCC._Visualization',
			'OCC._XCAFApp',
			'OCC._XCAFDoc',
			'OCC._XSControl'],
			
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
			 
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='bladepy_%s'% version,
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
			   a.binaries,
			   a.zipfiles,
			   a.datas,
			   strip=False,
			   upx=True,
			   name='BladePy_%s_standalone' % version)
