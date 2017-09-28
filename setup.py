from setuptools import setup, find_packages

setup(
    name='satfile_utils',
    version='0.4',
    description='Satellite Data File Utilities',
    author='Jonas Solvsteen',
    author_email='josl@dhi-gras.com',
    packages=find_packages(),
    install_requires=[
        'satmeta>=0.12'],
    dependency_links=[
        'https://github.com/DHI-GRAS/satmeta/archive/v0.12.tar.gz#egg=satmeta-0.12'])
