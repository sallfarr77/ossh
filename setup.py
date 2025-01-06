from setuptools import setup, find_packages

setup(
    name="ossh",
    version="1.0.0",
    description="Professional SSH Connection Manager",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Salman Al Farisi",
    author_email="sallman.alffarisi@gmail.com",
    url="https://github.com/sallfarr77/ossh",
    packages=find_packages(),
    py_modules=["ossh"],
    install_requires=[
        "rich>=13.9.4",
    ],
    entry_points={
        "console_scripts": [
            "ossh=ossh:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
    include_package_data=True,
)