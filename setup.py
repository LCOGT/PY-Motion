import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PY-Motion",
    version="5.0.0",
    author="Dave Douglass",
    author_email="ddouglass@lco.global",
    description="Python 3 library for Magellan Motion Processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LCOGT/PY-Motion",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "pyserial",
        "spidev",
    ],
)
