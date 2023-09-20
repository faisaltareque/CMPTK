from setuptools import setup, find_packages

setup(
    name="CMPTK",
    version="0.1",
    packages=find_packages(include=['CMPTK', 'CMPTK.*']),
    install_requires=[
        "nltk>=3.8.1",
        "Unidecode>=1.3.6",
    ],
)