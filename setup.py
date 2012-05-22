from setuptools import setup, find_packages

setup( name='session-cart',
	version='1.0.2',
	description='A session-stored cart for Django',
	author='Curtis Maloney',
	author_email='curtis@tinbrain.net',
	url='http://bitbucket.org/funkybob/session-cart/',
	keywords=['django', 'cms', 'e-commerce',],
	packages=find_packages(),
	zip_safe=False,
	classifiers = [
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Application Frameworks',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
)
