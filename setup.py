from setuptools import setup, find_packages

setup(
    name='clldutils',
    version='3.11.2.dev0',
    description='Utilities for programmatic data curation',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Robert Forkel',
    author_email='robert_forkel@eva.mpg.de',
    url='https://github.com/clld/clldutils',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'python-dateutil',
        'tabulate>=0.7.7',
        'colorlog',
        'attrs>=18.1.0',
        'csvw>=1.0',
    ],
    extras_require={
        'dev': ['flake8', 'wheel', 'twine'],
        'test': [
            'pytest>=5.4',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
        ],
    },
    license="Apache 2.0",
    zip_safe=False,
    keywords='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
