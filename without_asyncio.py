import requests

import psycopg2

from bs4 import BeautifulSoup

from config import (
    PASSWORD,
    HEADERS, 
    DB_NAME,
    AVITO,
    USER, 
    HOST, 
    # FILE,
    URL,
    )


CON = psycopg2.connect(
    host = HOST,
    user = USER,
    password = PASSWORD,
    database = DB_NAME
)


class Parser:   
    """"""
    
    @staticmethod
    def get_html(url, params=None):
        """"""
        print('sds')
        return requests.get(url, headers=HEADERS, params=params)
    
    @staticmethod
    def pagination_pag(html):
        """"""

        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find_all('span', class_='pagination-item-JJq_j')

        if pagination:
            return int(pagination[-2].text)
        else:
            return 1

    @staticmethod
    def get_content(html):
        """dgjsh"""

        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('a', class_ = 'link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH')

        all_urls = []    

        for item in items:
            all_urls.append(AVITO + item.get("href"))
        
        Parser.get_info(all_urls)
    
    @staticmethod
    def get_info(urls):
        """"""

        for url in urls:
            data = Parser.get_html(url)
            print('+++')
            soup = BeautifulSoup(data.text, 'html.parser')
            title = soup.find('span', class_ = 'title-info-title-text').text
            price = soup.find('span', class_ = 'js-item-price').text

            Parser.save_db(title, price)

    @staticmethod
    def save_db(title, price):
        """"""
        
        CON.cursor().execute(
            """INSERT INTO hous (title, price) VALUES
            ('{}', '{}');""".format(title, price)
        )
        CON.commit()


    #не обязатлеьно(для удобства) 
    # def save_file(items, path):
    #     with open(path, 'w', newline='') as file:
    #         writer = csv.writer(file, delimiter = ';')
    #         writer.writerow(['Объявление', 'Цена'])
    #         for item in items:
    #             writer.writerow([item['title'], item['price']])  
    
    def parse(self):
        """"""
        
        html = self.get_html(URL)
        if html.status_code == 200:
            # houses = []
            pages_count = self.pagination_pag(html.text)
            
            for page in range(1, pages_count + 1):
                print(f'Парсинг страницы {page} из {pages_count}')
                html = self.get_html(URL, params={'page': page})
                self.get_content(html.text)
            # save_file(houses, FILE)
            # print(f'Получено {len(houses)} предложений')
        else:
            print('ERROR')


if __name__ == '__main__':
    start_parsing = Parser
    start_parsing.parse(Parser)