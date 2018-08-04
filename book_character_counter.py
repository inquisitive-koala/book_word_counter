# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import unicodedata
from collections import defaultdict
import sys

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

def CountCharacters(book_path):
	text = open(book_path, 'rb').read()
	counter = defaultdict(int)
	for c in text.decode('utf-8'):
		if IsCJK(c):
			counter[c] += 1
	return counter

def CharactersByCount(book_path):
	counter = CountCharacters(book_path)
	pairs = zip(counter.keys(), counter.values())
	pairs.sort(key = lambda x: x[1], reverse = True)
	return pairs

if __name__ == '__main__':
	book_path = sys.argv[1]
	top_n = int(sys.argv[2])

	segmented_fulltext_path = 'segmented/fulltext-segmented.txt'
	sorted_pairs = CharactersByCount(book_path)

	for pair in sorted_pairs[:top_n]:
		print pair[1], '\t', pair[0]

	hist = numpy.histogram([pair[1] for pair in sorted_pairs], [n + 0.5 for n in range(0, 10)] + [1000,])
	print hist[0]

	num_top_words = 0
	for pair in sorted_pairs[:top_n]:
		num_top_words += pair[1]

	num_words = 0
	for pair in sorted_pairs:
		num_words += pair[1]

	print num_top_words
	print num_words
	print len(sorted_pairs)