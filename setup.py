from setuptools import find_packages,setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS project",
    version="0.1",
    author="Yasir Lakruwan",
    packages= find_packages(),
    install_requires = requirements,
)

