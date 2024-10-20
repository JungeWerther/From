from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="From - The Encapsulation Library",  # Replace with your own package name
    version="0.1.0",
    author="Seb Wiechers",
    author_email="",
    description="Encapsulation and decorators made easy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JungeWerther/From",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)