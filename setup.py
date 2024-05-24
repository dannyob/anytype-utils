from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt") as req_file:
        return req_file.read().splitlines()


setup(
    name="anytype-utils",
    version="0.1",
    packages=find_packages(),
    install_requires=read_requirements(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Danny O'Brien",
    author_email="danny@spesh.com",
    description="Unofficial Python interface to Anytype",
    url="http://github.com/dannyob/anytype-utils",
)
