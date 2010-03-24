from setuptools import setup, find_packages
 
setup(
    name='django-foafssl',
    version='0.1',
    description='foafssl tools for Django',
    author='Duy',
    author_email='duy@rhizomtik.net',
    url='http://git.rhizomatik.net/django-foafssl/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
#    package_data = {
#        'django_foafssl': [
##            'docs/intro.txt',
#            'templates/django_foafssl/foafssl/*.html'
#        ],
#    },
    include_package_data=True,
#    zip_safe=False,
#    install_requires=['python-foafcert', 'M2Crypto', 'pyOpenSSL', 'pysqlite'],
)

