import requests
import bs4


def search(query):
    url = 'http://baike.baidu.com/search'
    params = {
        'word': query,
        'pn': 0,
        'rn': 0,
        'enc': 'utf8'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

    response = requests.get(url, params=params, headers=headers)
    response.encoding='utf-8'
    return parse(response.text)


def parse(html_content):
    soup = bs4.BeautifulSoup(html_content, "lxml")
    result_links = soup.select('#body_wrapper  div.searchResult  dl dd a')
    url = result_links[0].attrs.get('href')
    title = soup.select('#body_wrapper  div.searchResult  dl dd a em')[0].get_text()
    content = soup.select('#body_wrapper  div.searchResult  dl dd p')[0].get_text()
    # get picture id
    url_content = requests.get(url)
    url_content.encoding = 'utf-8'
    url_soup = bs4.BeautifulSoup(url_content.text, "lxml")
    pictureUrl = url_soup.select('body div.body-wrapper div.content-wrapper div div.side-content div.summary-pic a img')[0].get('src')
    return formResult(title, content, pictureUrl, url)

def formResult(title, content, pictureUrl, url):
    return {
        'title': title,
        'content': content,
        'pictureUrl': pictureUrl,
        'url': url
    }

if __name__ == '__main__':
    search('')
