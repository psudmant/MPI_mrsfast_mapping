from distutils.core import setup 
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("add_positions_to_vect", ["add_positions_to_vect.pyx"])]
setup( 
	name = 'add pos numbers to array',
	cmdclass = {'build_ext': build_ext},
	ext_modules = ext_modules
	)
