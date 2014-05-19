from distutils.core import setup, Extension

module1 = Extension('dtrace',
                    define_macros = [('MAJOR_VERSION', '0'),
                                     ('MINOR_VERSION', '1')],
                    include_dirs = ['libusdt/'],
                    libraries = ['usdt'],
                    library_dirs = ['libusdt/'],
										extra_objects = ['libusdt/libusdt.a'],
                    sources = ['dtrace.c'])

setup (name = 'python-dtrace',
       version = '0.1',
       description = 'Python bindings for libusdt',
       author = 'Nahum Shalman',
       author_email = 'martin@v.loewis.de',
       url = 'http://github.com/nshalman/python-dtrace',
       long_description = '''
Python bindings for libusdt
''',
       ext_modules = [module1])
