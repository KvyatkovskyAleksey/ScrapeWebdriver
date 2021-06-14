import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="scrapy_webdriver",
	version="0.48",
	author="Aleksey Kvyatkovsky",
	author_email="kvyatkovsky@mail.ru",
	description="Class based on selenium webdriver.Firefox with methods  for scraping.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/KvyatkovskyAleksey/ScrapeWebdriver",
	packages=setuptools.find_packages(),
	install_requires=[
		'beautifulsoup4==4.9.3',
		'selenium==3.141.0',
		'webdriver-manager==3.4.2',
		'Scrapy==2.5.0'
    ],
	package_data={'': ['license.txt']},
	include_package_data=True,

	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],)