from distutils.core import setup


version = '0.5.dev'

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='eventsocket',
    version=version,
    py_modules=['eventsocket'],
    author=u'Fernando Fl\xf3rez',
    author_email='fernando@funciton.com',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description='This is a work in progress abstraction class to handle '
    'freeswitch\'s eventsocket command lines.',
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
