import os
from setuptools import setup, find_packages
import privateurl


setup(
    name='django-privateurl',
    version=privateurl.__version__,
    description='Django Private URL',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license='MIT',
    author='Igor Melnyk @liminspace',
    author_email='liminspace@gmail.com',
    url='https://github.com/liminspace/django-privateurl',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,  # because include static
    install_requires=[
        'django>=1.8,<2.3',
    ],
    keywords=[
        'django', 'url', 'private', 'private url', 'django-privateurl',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
    ],
)
