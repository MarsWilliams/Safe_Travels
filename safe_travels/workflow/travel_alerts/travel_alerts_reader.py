#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.arguments import Arguments
from reader.feed_reader import FeedReader
from bs4 import BeautifulSoup
import arrow
import logging

logger = logging.getLogger(__name__)


class TravelAlertsReader(object):

    def __init__(self,
                 alerts_path=None):
        self.reader = FeedReader(feed_path=alerts_path)
        self.feed = self.reader.read_feed()

    def read_travel_alerts(self):
        alerts = dict()
        alerts['metadata'] = self.feed['metadata']
        alerts['entries'] = self.get_parsed_entries(entries=self.feed['entries'])
        return alerts

    def get_parsed_entries(self, entries=None):
        parsed_entries = list()
        for entry in entries:
            parsed_entries.append(self.parse_entry(entry))
        return parsed_entries

    def parse_entry(self, entry=None):
        parsed_entry = dict()
        parsed_entry['title'] = entry.title
        parsed_entry['summary'] = self.parse_summary_detail(summary_detail=entry.summary_detail)
        parsed_entry['published'] = arrow.get(entry.published_parsed).format('YYYY-MM-DD HH:mm:ss')
        parsed_entry['links'] = self.parse_summary_links(value=entry.summary_detail.value)
        return parsed_entry

    def parse_summary_detail(self, summary_detail=None):
        parsed_summary = dict()
        parsed_summary['value'] = self.parse_summary_value(value=summary_detail.value)
        return parsed_summary

    @staticmethod
    def parse_summary_value(value=None):
        parsed_value = list()
        try:
            soup = BeautifulSoup(value, 'lxml')
            for p in soup.find_all('p'):
                if p.text:
                    parsed_value.append(p.text)
            return '\n'.join(parsed_value)
        except Exception as e:
            logger.error('Not valid xml format', e)

    @staticmethod
    def parse_summary_links(value=None):
        parsed_links = list()
        try:
            soup = BeautifulSoup(value, 'lxml')
            for a in soup.find_all('a'):
                link = dict()
                link['title'] = a.text
                link['link'] = a['href']
                parsed_links.append(link)
            return parsed_links
        except Exception as e:
            logger.error('Not valid xml format', e)


if __name__ == "__main__":
    args = Arguments()
    args.add_argument('--alerts')
    alerts_source = args.get('alerts', str())
    reader = TravelAlertsReader(alerts_path=alerts_source)
    reader.read_travel_alerts()
