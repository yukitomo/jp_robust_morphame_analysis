#!/usr/bin/python
#-*-coding:utf-8-*-
#2015-01-31 Yuki Tomo

import pickle, math, jctconv, string
from collections import defaultdict
from make_dict_obj import Morph
from morph_analizer_counts import *

def main():
	"""
	初期値
	P(c_i|c_i-1) = freq(c_i|c_i-1) / freq(c_i-1)
	P(v|c) = freq(v|c) / freq(c)

	誤り化初期値　0.01
	P(w|v) = 0.01
	P(v|v) = 0.99
	v → w : の展開するパターンを初期値として持っておく。
		freq(w|v) : mecab辞書の読みから頻度0のvalue値として持っておく


	学習の流れ
	1. mecabで解析しカウントした頻度(freq_d)の読み込み
	freq(c)_d, freq(v)_d
	freq(c_i|c_i-1)_d, freq(v|c)_d

	2.確率値の計算（あらかじめ計算しておく）
	P(c_i|c_i-1), P(v|c)

	3.現在のパラメータで誤り文を解析し、頻度を更新(freq_e)
	freq(c)_e, freq(v)_e
	freq(c_i|c_i-1)_e, freq(v|c)_e
	freq(w|v)_e

	4.確率値の再計算 (カウント数が変化した部分[分母が更新されたもの]だけ変更)
	P(c_i|c_i-1), P(v|c)
	P(w|v)

	5. 3,4を繰り返す

	input : 大量の日本語誤り文が格納されたファイル

	"""

	#1.初期頻度_dの読み込み
	iddef = load_2colums(open(dict_dir + "left-id.def","r")," ") #mecabはr,l同じID
	rpdic = pickle.load(open(pkl_dir + "ipadic_read_pron_dict.pkl", "r"))

	#毎日新聞
	pkl_dir = "/Users/yukitomo/Research/jp_robust_morphame_analysis/pkl_data/"
	c_freq_d = pickle.load(open(pkl_dir + "mainichi_posid_unigram_counts.pkl","r")) #freq(c)
	cc_freq_d = pickle.load(open(pkl_dir + "mainichi_posid_bigram_counts.pkl","r")) #freq(c_i|c_i-1)
	vc_freq_d = pickle.load(open(pkl_dir + "mainichi_posid_word_counts.pkl","r")) #freq(v|c)

	#dict check
	#print cc_freq_d
	#for k1, v1 in cc_freq_d.items():
	#	for k2, v2 in v1.items():
	#		if k1 == "B":
	#			print k1,k2,v2
	#print vc_freq_d

	#w_v_freq_d : 存在しないがとりあえず格納
	v_freq_d = {}
	wv_freq_d = defaultdict(dict)

	#Freq クラスに格納 初期頻度freq_d
	freq_d = Freq(c_freq_d, cc_freq_d, vc_freq_d, wv_freq_d, v_freq_d)

	#2.初期頻度_dから確率値の計算をし、コスト（対数）に変換
	cc_cost = freq_d.calc_cost("cc", 10)
	#vc_cost = freq_d.calc_cost("vc", 10) #文字列から検索するために、morphオブジェクト型に変更する必要あり



	#デコードの確認
	#文の入力
	input_sent = raw_input('input a sentence\n')

	#ラティスの生成
	lm = Lattice_Maker(wdic, rpdic, wvcos, cccos, iddef)
	lattice = lm.create_lattice(input_sent)
	#pickle.dump(lattice, open(pkl_dir + "lattice_gohanwotaberu.pkl","w"))

	#ビタビによる最適な系列の決定
	best_sequence = lm.viterbi(lattice)

	#最適系列の出力
	lm.show_best_sequence(best_sequence)
	print lm.return_best_sequence_counts(best_sequence)

	
	
	#単語辞書checker
	"""
	for windex, morph_list in wdic.items():
		print windex
		for morph in morph_list:
			morph.showinfo()
	"""
		

	"""
	
	posid_unigram_freq : 品詞の頻度
	posid_bigram_freq : 品詞バイグラムの頻度
	posid_word_freq : 品詞と単語の組み合わせの頻度
	




	#Eステップで計算される頻度
	posid_unigram_freq_e = {}
	posid_bigram_freq_e = defaultdict(dict)
	posid_word_freq_e = defaultdict(dict)
	wvcos = load_3colums_string(open(dict_dir + "wv_cost.def","r"),"\t")

	alpha = 0.01


	#文の入力
	#input_sent = raw_input('input a sentence\n')

	
	#大量の文が格納されたファイルの入力
	sents_file = open()

	for sent in sents_file:
		#増えた頻度の項目のみパラメータの更新
		wdic = 
		rpdic = 
		cccos = 
		#?
		wvcos =

		#ラティスの生成
		lm = Lattice_Maker(wdic, rpdic, wvcos, cccos, iddef)
		lattice = lm.create_lattice(input_sent)
		#pickle.dump(lattice, open(pkl_dir + "lattice_gohanwotaberu.pkl","w"))
		
		#ビタビによる最適な系列の決定
		best_sequence = lm.viterbi(lattice)
		
		#最適系列の出力 : 品詞単語の組み合わせ、wvの組み合わせ、品詞bigram 
		lm.return_best_sequence_counts(best_sequence)
	
	
	#生成されたラティスの確認
	for k1, v in lattice.items():
		for k2, node_list in v.items():
			print k1, k2
			for node in node_list:
				node.showinfo()
	"""


if __name__ == '__main__':
	main()