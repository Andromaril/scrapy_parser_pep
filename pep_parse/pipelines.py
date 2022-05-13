import csv
import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).parent


class PepParsePipeline:

    def open_spider(self, spider):
        self.counts = {'Active': 0, 'Final': 0, 'Superseded': 0,
                       'Deferred': 0, 'Rejected': 0,
                       'Withdrawn': 0, 'April Fool!': 0,
                       'Draft': 0, 'Final': 0, 'Accepted': 0, }

    def process_item(self, item, spider):
        try:
            status = item['status']
        except KeyError:
            print('Такого ключа нет!')
        self.counts[status] = self.counts.get(status) + 1
        return item

    def close_spider(self, spider):
        downloads_dir = BASE_DIR / 'results'
        now_date = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file = f'status_summary_{now_date}.csv'
        path = downloads_dir / file
        with open(path, mode='w', encoding='utf-8') as csvfile:
            header = ['Статус', 'Количество']
            pep = self.counts.items()
            total = ['Total', sum(self.counts.values())]
            spamwriter = csv.writer(
                csvfile,
                quoting=csv.QUOTE_MINIMAL
            )
            spamwriter.writerows([
                header,
                *pep,
                total,
            ])
