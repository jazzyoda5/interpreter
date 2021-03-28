from setuptools import setup, find_packages

setup(
    name='interpreter',
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where='interpreter'),
    package_dir={'': 'interpreter'}
)