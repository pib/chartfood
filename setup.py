from setuptools import setup, find_packages

setup(
    name="chartfood",
    version="0.1",
    description="Tools for making stuff to feed to graphs/charts",
    author="Paul Bonser",
    install_requires=['six', 'pyramid'],
    license="Apache 2.0",
    url="https://github.com/pib/chartfood",
    packages=find_packages()
)
