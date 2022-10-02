from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'Practice Competitive Programming directly from Terminal'
LONG_DESCRIPTION = 'CLI to fetch questions and contests from Codeforces, Codechef and AtCoder'

# Setting up
setup(
    name="codehut",
    version=VERSION,
    author="Coffee Beans",
    author_email="18raj06@gamil.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'beautifulsoup4', 'lxml'],
    keywords=['python', 'cli', 'competitive-programming', 'cp', 'codeforces', 'codechef', 'atcoder', 'cf', 'cc', 'codehut'],
    classifiers=[
        "Development Status :: Production",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        # "Operating System :: Unix",
        # "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)