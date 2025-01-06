from setuptools import setup, find_packages

setup(
    name="ossh",
    version="1.0.0",
    description="A Python tool for SSH-related utilities.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Salman Al Farisi",
    author_email="sallman.alffarisi@gmail.com",
    url="https://github.com/sallfarr77/ossh",
    py_modules=["ossh"],
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "ossh=ossh:main",  
        ],
    },
    license="MIT",
)
