from setuptools import setup, find_packages

setup(
    name="ethio-calendar",
    version="1.0.0",
    author="Mengistu Getie",
    author_email="mengist.dev@gmail.com",
    description="Ethiopian Calendar with conversions to/from Gregorian",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mgemoraw/ethio-calendar",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.8",
    include_package_data=True,
)
