from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def get_all_website_links(url):
	urls = set()
	domain_name = urlparse(url).netloc  # attr netloc keeps domain name
	session = HTMLSession()  # create session for webapp to work
	response = session.get(url)  # to get site info
	try:
		response.html.render()
	except:
		pass
	
	soup = BeautifulSoup(response.html.html, 'html.parser').findAll('a')
	for a_tag in soup:
		href = a_tag.attrs.get('href')
		if href == '' or href is None:
			continue
		href = urljoin(url, href)
		parsed_href = urlparse(href)
		href = parsed_href.scheme + '://' + parsed_href.netloc + parsed_href.path
		if href in internal_urls:
			continue
		if domain_name not in href:
			if href not in external_urls:
				print(f'[+] External Link: {href}')
				external_urls.add(href)
			continue
		print(f'[+] Internal Link: {href}')
		urls.add(href)
		internal_urls.add(href)
	return urls


def crawl(url):  # crawler gets data from website
	print(f' [+] Crawling: {url}')
	links = get_all_website_links(url)
	for link in links:
		crawl(link)


if __name__ == '__main__':
	internal_urls = set()
	external_urls = set()
	
	crawl('https://domain.com')
	with open(f'links.txt', 'w') as f:
		print('INTERNAL:', file=f)
		for internal_link in internal_urls:
			print(internal_link.strip(), file=f)
		print('EXTERNAL:')
		for external_link in external_urls:
			print(external_link.strip(), file=f)
