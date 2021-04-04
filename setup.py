import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto-portfolio",
    version="0.0.1",
    author="Billy Ferguson",
    author_email="william.d.ferg@gmail.com",
    description="A stats and ML based auto portfolio generator with predictions and backtesting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fergyfresh/auto-portfolio",
    project_urls={
        "Bug Tracker": "https://github.com/fergyfresh/auto-portfolio/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "auto_portfolio"},
    packages=setuptools.find_packages(where="auto_portfolio"),
    python_requires=">=3.8",
)