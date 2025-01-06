from setuptools import setup

setup(
    name="ossh",
    version="1.0.0",
    description="Professional SSH Connection Manager",
    author="Salman Al Farisi",
    author_email="sallman.alffarisi@gmail.com",
    url="https://github.com/sallfarr77/ossh",
    package_dir={"": "src"},
    packages=["ossh"],
    install_requires=["rich>=13.9.4"],
    entry_points={
        "console_scripts": [
            "ossh=ossh:main",
        ],
    },
    python_requires=">=3.6",
    license="MIT",
)