#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.arguments import Arguments
from utils.strings import remove_escape_characters, parse_url, build_url_from_parts
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
        parsed_entry['source'] = entry.link
        parsed_entry['summary'] = self.parse_summary_detail(summary_detail=entry.summary_detail)
        parsed_entry['published'] = arrow.get(entry.published_parsed).format('YYYY-MM-DD HH:mm:ss')
        parsed_entry['links'] = self.get_parsed_summary_links(value=entry.summary_detail.value)
        parsed_entry['country'] = self.get_country(links=parsed_entry['links'])
        return parsed_entry

    def parse_summary_detail(self, summary_detail=None):
        parsed_summary = dict()
        parsed_summary['value'] = self.parse_summary_value(value=summary_detail.value)
        return parsed_summary

    def parse_summary_value(self, value=None):
        parsed_value = list()
        try:
            soup = BeautifulSoup(value, 'lxml')
            for p in soup.find_all('p'):
                if p.text:
                    parsed_value.append(
                        remove_escape_characters(value=p.text)
                    )
            return '\n'.join(parsed_value)
        except Exception as e:
            logger.error('Not valid xml format', e)

    def get_parsed_summary_links(self, value=None):
        parsed_links = list()
        try:
            soup = BeautifulSoup(value, 'lxml')
            for a in soup.find_all('a'):
                link = dict()
                link['title'] = a.text
                link['link'] = self.parse_link(link=a['href'])
                parsed_links.append(link)
            return parsed_links
        except Exception as e:
            logger.error('Not valid xml format', e)

    def parse_link(self, link=None):
            parsed_link = parse_url(link).__dict__
            formatted_link = []
            if not parsed_link['scheme']:
                formatted_link.append('http')
            else:
                formatted_link.append(parsed_link['scheme'])
            if not parsed_link['netloc']:
                formatted_link.append('travel.state.gov')
            else:
                formatted_link.append(parsed_link['netloc'])
            formatted_link.extend([
                parsed_link['path'],
                parsed_link['params'],
                parsed_link['query'],
                parsed_link['fragment']
            ])
            return build_url_from_parts(formatted_link)

    def get_country(self, links=None):
        for link in links:
            if link['link'].find('/country/') != -1:
                try:
                    return link['link'].split('/country/')[1].split('.html')[0].replace('-', ' ')
                except Exception as e:
                    logger.error(e)

    def get_region(self):
        pass


if __name__ == "__main__":
    args = Arguments()
    args.add_argument('--alerts')
    alerts_source = args.get('alerts', str())
    reader = TravelAlertsReader(alerts_path=alerts_source)
    reader.read_travel_alerts()
