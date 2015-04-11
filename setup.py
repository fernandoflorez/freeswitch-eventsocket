from setuptools import setup


version = '0.5.dev'

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='freeswitch-eventsocket',
    version=version,
    py_modules=['eventsocket'],
    author=u'Fernando Fl\xf3rez',
    author_email='fernando@funciton.com',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description='This is a work in progress abstraction class to handle '
    'freeswitch\'s eventsocket command lines.',
    long_description=long_description,
    url='https://github.com/fernandoflorez/freeswitch-eventsocket'
)
