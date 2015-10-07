#-*- coding: utf-8 -*-
from datetime import datetime
import bs4, nltk, os, pytz, re, time, urlparse
from nltk.corpus import wordnet
import numpy, random
from bs4 import BeautifulSoup
#from pattern.en import pluralize, singularize
from stop_words import get_stop_words
from nltk.tree import Tree
from bs4.element import NavigableString
from titlecase import titlecase


def getDateFromTextArabic(text):
    d = {}

    #january
    d[u'\u0643\u0627\u0646\u0648\u0646 \u0627\u0644\u062b\u0627\u0646\u064a'] = 1
    d[u'\u064a\u0646\u0627\u064a\u0631'] = 1
    d[u'\u0623\u064a \u0627\u0644\u0646\u0627\u0631'] = 1
    d[u'\u062c\u0627\u0646\u0641\u064a'] = 1
    d[u'\u064a\u0646\u0627\u064a\u0631'] = 1

    #february
    d[u'\u0634\u0628\u0627\u0637'] = 2
    d[u'\u0641\u0628\u0631\u0627\u064a\u0631'] = 2
    d[u'\u0627\u0644\u0646\u0648\u0627\u0631'] = 2
    d[u'\u0641\u064a\u0641\u0631\u064a'] = 2

    # march
    d[u'\u0622\u0630\u0627\u0631'] = 3
    d[u'\u0645\u0627\u0631\u0633'] = 3
    d[u'\u0627\u0644\u0631\u0628\u064a\u0639'] = 3
    d[u'\u0645\u0627\u0631\u0633'] = 3

    #april
    d[u'\u0646\u064a\u0633\u0627\u0646'] = 4
    d[u'\u0623\u0628\u0631\u064a\u0644'] = 4
    d[u'\u0625\u0628\u0631\u064a\u0644'] = 4
    d[u'\u0627\u0644\u0637\u064a\u0631'] = 4
    d[u'\u0623\u0641\u0631\u064a\u0644'] = 4
 
    #may
    d[u'\u0623\u064a\u0627\u0631'] = 5
    d[u'\u0645\u0627\u064a\u0648'] = 5
    d[u'\u0627\u0644\u0645\u0627\u0621'] = 5
    d[u'\u0645\u0627\u064a'] = 5

    #june
    d[u'\u062d\u0632\u064a\u0631\u0627\u0646'] = 6
    d[u'\u064a\u0648\u0646\u064a\u0648'] = 6
    d[u'\u064a\u0648\u0646\u064a\u0629'] = 6
    d[u'\u0627\u0644\u0635\u064a\u0641'] = 6
    d[u'\u062c\u0648\u0627\u0646'] = 6

    #july
    d[u'\u062a\u0645\u0648\u0632'] = 7
    d[u'\u064a\u0648\u0644\u064a\u0648'] = 7
    d[u'\u064a\u0648\u0644\u064a\u0629'] = 7
    d[u'\u0646\u0627\u0635\u0631'] = 7
    d[u'\u062c\u0648\u064a\u0644\u064a\u0629'] = 7
    d[u'\u064a\u0648\u0644\u064a\u0648\u0632'] = 7

    #august
    d[u'\u0622\u0628'] = 8
    d[u'\ufe82\ufe91'] = 8
    d[u'\u0623\u063a\u0633\u0637\u0633'] = 8
    d[u'\u0647\u0627\u0646\u064a\u0628\u0627\u0644'] = 8
    d[u'\u0623\u0648\u062a'] = 8
    d[u'\u063a\u0634\u062a'] = 8

    #september
    d[u'\u0623\u064a\u0644\u0648\u0644'] = 9
    d[u'\u0633\u0628\u062a\u0645\u0628\u0631'] = 9
    d[u'\u0627\u0644\u0641\u0627\u062a\u062d'] = 9
    d[u'\u0633\u0628\u062a\u0645\u0628\u0631'] = 9
    d[u'\u0634\u062a\u0645\u0628\u0631'] = 9

    #october
    d[u'\u062a\u0634\u0631\u064a\u0646 \u0627\u0644\u0623\u0648\u0644'] = 10
    d[u'\u0623\u0643\u062a\u0648\u0628\u0631'] = 10
    d[u'\u0627\u0644\u062a\u0645\u0648\u0631'] = 10
    d[u'\u0627\u0644\u062b\u0645\u0648\u0631'] = 10
    d[u'\u0623\u0643\u062a\u0648\u0628\u0631'] = 10

    #november
    d[u'\u062a\u0634\u0631\u064a\u0646 \u0627\u0644\u062b\u0627\u0646\u064a'] = 11
    d[u'\u0646\u0648\u0641\u0645\u0628\u0631'] = 11
    d[u'\u0627\u0644\u062d\u0631\u062b'] = 11
    d[u'\u0646\u0648\u0641\u0645\u0628\u0631'] = 11
    d[u'\u0646\u0648\u0646\u0628\u0631'] = 11

    #december
    d[u'\u0643\u0627\u0646\u0648\u0646 \u0627\u0644\u0623\u0648\u0644'] = 12
    d[u'\u062f\u064a\u0633\u0645\u0628\u0631'] = 12
    d[u'\u0627\u0644\u0643\u0627\u0646\u0648\u0646'] = 12
    d[u'\u062f\u064a\u0633\u0645\u0628\u0631'] = 12
    d[u'\u062f\u062c\u0645\u0628\u0631'] = 12

    result = re.search(ur'(?P<day>\d{1,2}) (?P<month>\u0646\u064a\u0633\u0627\u0646|\u0627\u0644\u0643\u0627\u0646\u0648\u0646|\u0623\u0643\u062a\u0648\u0628\u0631|\u0623\u064a\u0644\u0648\u0644|\u0627\u0644\u0645\u0627\u0621|\u0623\u0628\u0631\u064a\u0644|\u0622\u0630\u0627\u0631|\u0647\u0627\u0646\u064a\u0628\u0627\u0644|\u0627\u0644\u062b\u0645\u0648\u0631|\u064a\u0648\u0646\u064a\u0648|\u0627\u0644\u0641\u0627\u062a\u062d|\u064a\u0646\u0627\u064a\u0631|\u064a\u0648\u0644\u064a\u0629|\u0645\u0627\u064a|\u062c\u0627\u0646\u0641\u064a|\u0645\u0627\u0631\u0633|\u0641\u064a\u0641\u0631\u064a|\u0627\u0644\u0646\u0648\u0627\u0631|\u0623\u0641\u0631\u064a\u0644|\u0641\u0628\u0631\u0627\u064a\u0631|\u0627\u0644\u0631\u0628\u064a\u0639|\u062a\u0634\u0631\u064a\u0646 \u0627\u0644\u062b\u0627\u0646\u064a|\u062f\u062c\u0645\u0628\u0631|\u0634\u0628\u0627\u0637|\u0646\u0627\u0635\u0631|\u064a\u0648\u0644\u064a\u0648|\u0627\u0644\u0637\u064a\u0631|\u0646\u0648\u0641\u0645\u0628\u0631|\u0623\u0648\u062a|\u062c\u0648\u0627\u0646|\u0622\u0628|\u0623\u063a\u0633\u0637\u0633|\u062c\u0648\u064a\u0644\u064a\u0629|\u062f\u064a\u0633\u0645\u0628\u0631|\u0633\u0628\u062a\u0645\u0628\u0631|\u0623\u064a \u0627\u0644\u0646\u0627\u0631|\u0627\u0644\u062a\u0645\u0648\u0631|\u0646\u0648\u0646\u0628\u0631|\u0645\u0627\u064a\u0648|\u0627\u0644\u062d\u0631\u062b|\u062a\u0645\u0648\u0632|\u0623\u064a\u0627\u0631|\u0634\u062a\u0645\u0628\u0631|\u062a\u0634\u0631\u064a\u0646 \u0627\u0644\u0623\u0648\u0644|\u063a\u0634\u062a|\u062d\u0632\u064a\u0631\u0627\u0646|\u0627\u0644\u0635\u064a\u0641|\u0643\u0627\u0646\u0648\u0646 \u0627\u0644\u062b\u0627\u0646\u064a|\u0625\u0628\u0631\u064a\u0644|\u064a\u0648\u0644\u064a\u0648\u0632|\u0643\u0627\u0646\u0648\u0646 \u0627\u0644\u0623\u0648\u0644|\u064a\u0648\u0646\u064a\u0629|\ufe82\ufe91)\u060c (?P<year>\d{4})', text)
    if result:
        return datetime(int(result.group("year")), d[result.group("month")], int(result.group("day")), tzinfo=pytz.UTC)