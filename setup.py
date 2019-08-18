import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="scrapy_webdriver",
	version="0.34",
	author="Aleksey Kvyatkovsky",
	author_email="kvyatkovsky@mail.ru",
	description="Class based on selenium webdriver.Firefox with methods\
	 for scraping.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/KvyatkovskyAleksey/ScrapeWebdriver",
	packages=setuptools.find_packages(),
	install_requires=[
        'beautifulsoup4==4.7.1',
		'bs4==0.0.1',
		'pkg-resources==0.0.0',
		'selenium==3.141.0',
		'soupsieve==1.9.2',
		'urllib3==1.25.3'
    ],
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],)