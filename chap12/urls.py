from urls_utils import gen_from_urls

urls = ('http://headfirstlabs.com', 'http://oreilly.com', 'http://twitter.com')
for resp_len, status, url, in gen_from_urls(urls):
    print(resp_len, '->', status, '->', url)