from setuptools import setup, find_packages

DEPENDENCIES = [
    "mypy",
    "pyyaml",
    "pylint",
    "termcolor"
]

readme = open('README.md', 'r')
README_TEXT = readme.read()
readme.close()

setup(
    name='skorovarka',
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['skvk=skorovarka.main:main'],
    },
    setup_requires=[],
    install_requires=DEPENDENCIES,
    version="1.0.0",
    description="Speed up creation of repositories from templates",
    long_description=README_TEXT,
    keywords="template,repository,deployment",
    author="Krzysztof J. Czarnecki",
    author_email="kcjzarne@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)