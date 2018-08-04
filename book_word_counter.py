# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import unicodedata
from collections import defaultdict
import sys
import numpy

def PrintBook():
	page_pattern = 'priest-zhenhun/priest-zhenhun-%i.html'
	num_pages = 122

	for i in range(1, num_pages + 1):
		page_path = page_pattern % i
		html = open(page_path, 'rb').read()
		content = BeautifulSoup(html, 'html.parser').body.find("div", {'id': 'BookContent'}).get_text()
		content = content.strip()
		print content.encode('utf-8')

def IsCJK(character):
	try:
		return unicodedata.name(character).startswith('CJK UNIFIED IDEOGRAPH')
	except ValueError, v:
		return False

def CountWords(book_path):
	text = open(book_path, 'rb').read()
	words = text.split()

	counter = defaultdict(int)
	for w in words:
		if all(IsCJK(c) for c in w.decode('utf-8')):
			counter[w] += 1
	return counter

def WordsByCount(book_path, counts):
	text = open(book_path, 'rb').read()
	words = set(text.split())
	pairs = [(w, counts[w]) for w in words]
	pairs.sort(key = lambda x: x[1], reverse = True)
	return pairs

def ReadWords(words_path):
	lines = open(words_path, 'rb').readlines()
	return set([l.strip() for l in lines])

if __name__ == '__main__':
	book_path = sys.argv[1]
	top_n = int(sys.argv[2])
	fulltext_path = 'segmented/fulltext-segmented.txt'
	known_words_path = 'known_words.txt'

	global_counts = CountWords(fulltext_path)
	local_counts = CountWords(book_path)
	known_words = ReadWords(known_words_path)

	globally_sorted_words = sorted(local_counts.keys(), key = lambda w: global_counts[w], reverse = True)
	filtered_words = [w for w in globally_sorted_words if w not in known_words]
	top_words = filtered_words[:top_n]
	top_words.sort(key = lambda w: local_counts[w], reverse = True)

	# Print words
	for word in top_words:
		print local_counts[word], '\t', word

	# Stats
	print sum(local_counts[w] for w in top_words + list(known_words))
	print sum(local_counts.values())
	print len(local_counts)
