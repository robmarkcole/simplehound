from setuptools import setup, find_packages

VERSION = "0.3"

REQUIRES = ["requests"]

setup(
    name="simplehound",
    version=VERSION,
    url="https://github.com/robmarkcole/simplehound",
    author="Robin Cole",
    author_email="robmarkcole@gmail.com",
    description="Unofficial python API for Sighthound",
    install_requires=REQUIRES,
    packages=find_packages(exclude=['tests','tests.*']),
    license="Apache License, Version 2.0",
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
