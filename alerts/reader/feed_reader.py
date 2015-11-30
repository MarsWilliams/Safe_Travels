#!/usr/bin/env python
# -*- coding: utf-8 -*-
import feedparser
from config.config import Config
from utils.arguments import Arguments


class FeedReader(object):

    def __init__(self,
                 feed_path=None):
        self.config = Config()
        self.feed_path = feed_path if feed_path else self.config.path.get('feed_path', str())
        self.raw_feed = self.get_feed()

    def get_feed(self):
        return feedparser.parse(self.feed_path)

    def get_feed_metadata(self):
        metadata = dict()
        metadata['title'] = self.get_title()
        metadata['subtitle'] = self.get_subtitle()
        metadata['description'] = self.get_description()
        return metadata

    def get_title(self):
        return self.raw_feed.feed.title

    def get_subtitle(self):
        return self.raw_feed.feed.subtitle

    def get_description(self):
        return self.raw_feed.feed.description

    def get_feed_entries(self):
        return self.raw_feed.entries

    def read_feed(self):
        feed = dict()
        feed['metadata'] = self.get_feed_metadata()
        feed['entries'] = self.get_feed_entries()
        return feed


if __name__ == "__main__":
    args = Arguments()
    args.add_argument('--feed')
    feed_source = args.get('feed', str())
    reader = FeedReader(feed_path=feed_source)
