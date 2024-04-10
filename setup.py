from setuptools import setup
import setuptools
setup(
    name="pbct-api",
    version='2.7.62',
    author="CintagramABP",
    description="PBCT API",
    long_description="BCSFE_Python personal api",
    url="",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "colored==1.4.4",
        "tk",
        "python-dateutil",
        "requests",
        "pyyaml",
        "aiohttp",
		"bcsfe-discord==2.7.62",
		"colorama"
    ],
    include_package_data=True,
    extras_require={
        "testing": [
            "pytest",
            "pytest-cov",
        ],
    },
    package_data={"pbctapi": ["py.typed"]},
    flake8={"max-line-length": 160},
)
