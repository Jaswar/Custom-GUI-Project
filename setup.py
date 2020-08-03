import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="customGUI",
    version="1.0.7",
    author="Jan Warchocki",
    author_email="janwarchocki@gmail.com",
    description="Maker for custom-built GUI for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jaswar/Custom-GUI-Project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pygame'],
    python_requires='>=3.6'
)