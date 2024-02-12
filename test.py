from urllib.parse import urlparse

def standardise_url(url):
    parsed_url = urlparse(url)
    components = parsed_url.netloc.split(".")
    final_url = 'www.' + \
        parsed_url.netloc if not parsed_url.netloc.startswith(
            'www.') and len(components)==2 else parsed_url.netloc
    print(parsed_url.scheme + '://' + final_url + parsed_url.path)
    return parsed_url.scheme + '://' + final_url + parsed_url.path

def get_base_url(url):
    parsed_url = urlparse(url)
    components = parsed_url.netloc.split(".")
    final_url = 'www.' + \
        parsed_url.netloc if not parsed_url.netloc.startswith(
            'www.') and len(components)==2 else parsed_url.netloc
    print(final_url)
    return final_url

standardise_url("https://www.sirmax.com/en/sitemaps/pages/sitemap.xml")
get_base_url("https://www.sirmax.com/en/sitemaps/pages/sitemap.xml")