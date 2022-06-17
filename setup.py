import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='hdlc',
    version='0.0.1',
    author='Submer Inc',
    description='A Python library for encoding and decoding HDLC frames and facilitating transport agnostic communication',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/submer-crypto/hdlc',
    license='ISC',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
