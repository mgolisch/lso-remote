from setuptools import setup

setup(
    name='lso-remote',
    version='0.1',
    py_modules=['lso_remote'],
    install_requires=[
        'flask-sockets','requests'
    ],
    entry_points='''
        [console_scripts]
        lso-remote=lso_remote:cli
    ''',
)