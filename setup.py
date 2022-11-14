from setuptools import setup, find_packages

VERSION = '0.0.0'
DESCRIPTION = 'Practice Competitive Programming directly from Terminal'
LONG_DESCRIPTION = 'CLI to fetch questions and contests from Codeforces'

# Setting up
setup(
    name="codehutt",
    version=VERSION,
    author="Coffee Beans",
    author_email="18raj06@gamil.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    # package_dir = {"": ""},
    packages=find_packages(),
    install_requires=['opencv-python', 'bs4', 'lxml', 'requests', 'subprocess', 'os', 'random', 'json', 'pytest-shutil', 'pathlib', 'argparse'],
    keywords=['python', 'cli', 'competitive-programming', 'cp', 'codeforces', 'codechef', 'atcoder', 'cf', 'cc', 'codehut'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        # "Operating System :: Unix",
        # "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)