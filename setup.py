from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
# Thanks https://github.com/pypa/sampleproject/blob/main/setup.py

setup(  name='binse',
        description='A binary searching tool',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/Thaelz/binse',
        keywords='binary, search, hex',
        version='0.11',
        python_requires='>=3.5, <4',
        package_dir={'binse': 'src'},
        packages=['binse'],
        install_requires=[
            'rich',
            'lief'
        ],
        entry_points={
          'console_scripts': [
              'binse=binse.binse:main',
          ],
        },
)