import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="efj_convert",
    version="0.1",
    author="Jon Hurst",
    author_email="jon.a@hursts.org.uk",
    description="Convert EFJ files into FCL compliant logbooks and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        ("License :: OSI Approved :: "
         "GNU General Public License v3 or later (GPLv3+)"),
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        "nightflight",
        "efj_parser"
    ],
    package_data={
        "efj_convert": ["summary-template.html",
                        "logbook-template.html"]
    },
    entry_points={
        "console_scripts": [
            "efj = efj_convert.cli:main"
        ]
    },
)
