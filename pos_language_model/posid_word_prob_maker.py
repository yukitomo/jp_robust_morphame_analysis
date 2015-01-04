#!/usr/bin/python
#-*-coding:utf-8-*-

import sys,pickle
from collections import defaultdict

def trasition_probability(pair_counts):
	pair_prob = defaultdict(dict)
	a_c = 0
	for a in pair_counts.keys():
		for ab_c in pair_counts[a].values():
			a_c +=  ab_c
		for b,ab_c in pair_counts[a].items():
			ab_prob = float(ab_c) / a_c
			pair_prob[a][b] = ab_prob
		a_c = 0
	return pair_prob

def main():
	posid_bigram_counts = pickle.load(open(sys.argv[1]))
	posid_word_counts = pickle.load(open(sys.argv[2]))

	posid_bigram_prob = trasition_probability(posid_bigram_counts)
	posid_word_prob = trasition_probability(posid_word_counts)

	"""
	for c in posid_word_prob.keys():
		for w,v in posid_word_prob[c].items():
			print c,w,v
	for c_p in posid_bigram_prob.keys():
		for c_n,v in posid_bigram_prob[c_p].items():
			print c_p,c_n,v
	"""

	pickle.dump(posid_bigram_prob,open("mainichi_posid_bigram_prob.pkl","w"))
	pickle.dump(posid_word_prob,open("mainichi_posid_word_prob.pkl","w"))

if __name__ == '__main__':
	main()