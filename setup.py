from setuptools import setup

# Run the Setup
setup(
    name='SpotiClick',
    version='0.1',
    # package_dir={'': '.'},
    packages=['spotipy_lib', 'configuration'],
    py_modules=['main'],
    data_files=[('', ['configuration/yml_schema.json'])],
    entry_points={
        'console_scripts': [
            'spoticlick=main:main',
        ]
    },
    url='https://github.com/drkostas/SpotiCLick',
    license='GNU General Public License v3.0',
    author='drkostas',
    author_email='georgiou.kostas94@gmail.com',
    description='An app that clicks a physical button whenever Spotify starts playing on a target device.'

)
