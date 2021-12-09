import setuptools
with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name = 'covid_dashboard-pkg-adshep', # Replace with your own username
    version = '0.0.1',
    author = 'Adam Sheppard',
    author_email = 'as1606@exeter.ac.uk',
    description = 'A flask dashboard which lets you see/schedule live covid data',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Adshep/execovid_dashboard",
    packages = setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


