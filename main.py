import bs4
import requests
import re
from fake_headers import Headers


class ArticleSearcher:

    def __init__(self, keywords):
        assert isinstance(keywords, list), 'Переданное значение не является списком!'

        self.keywords = keywords

        self.base_url = 'https://habr.com'
        self.url = self.base_url + '/ru/all/'

        self.headers = Headers(browser='chrome', os='mac', headers=True).generate()

    def _find_keywords(self, title, preview):
        for i, _ in enumerate(self.keywords):
            if re.findall(self.keywords[i], title) or re.findall(self.keywords[i], preview):
                return True
            else:
                return False

    def search_articles(self):
        response = requests.get(self.url, headers=self.headers)

        if response.status_code != 200:
            return 'Ошибка: повторите попытку через некоторое время!'

        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        articles = soup.find_all('article')

        for article in articles:
            title = article.find('h2').find('span')
            preview = article.find(class_='article-formatted-body article-formatted-body '
                                          'article-formatted-body_version-2')

            if preview is None or title is None:
                continue
            else:
                title = title.text
                preview = preview.text

            if self._find_keywords(title=title, preview=preview):
                date = article.find('time').attrs['title']
                href = article.find('h2').find('a').attrs['href']

                result = f'{date} - {title} - {self.base_url + href}'

                print(result)


KEYWORDS = ['Python', 'python']

if __name__ == '__main__':
    searcher = ArticleSearcher(keywords=KEYWORDS)
    searcher.search_articles()
