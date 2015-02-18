#!/usr/bin/python
#-*-coding:utf-8-*-
#2015-01-31 Yuki Tomo

import pickle, math, jctconv, string
from collections import defaultdict
from make_dict_obj import Morph
from morph_analizer_counts import *

def main():
	"""
	posid_unigram_freq : 品詞の頻度
	posid_bigram_freq : 品詞バイグラムの頻度
	posid_word_freq : 品詞と単語の組み合わせの頻度

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

	#--------------------------初期設定------------------------------------

	#品詞id, 読みの辞書の読み込み
	dict_dir = "/Users/yukitomo/Research/jp_robust_morphame_analysis/data/mecab-ipadic-2.7.0-20070801-utf8/"
	pkl_dir = "/Users/yukitomo/Research/jp_robust_morphame_analysis/pkl_data/"

	id_def = load_2colums(open(dict_dir + "left-id.def","r")," ") #mecabはr,l同じID
	read_pron_dic = pickle.load(open(pkl_dir + "ipadic_read_pron_dict.pkl", "r"))

	#1.初期頻度_dの読み込み
	#毎日新聞
	pkl_dir = "/Users/yukitomo/Research/jp_robust_morphame_analysis/pkl_data/"
	c_freq_d = pickle.load(open(pkl_dir + "mainichi_posid_unigram_counts.pkl","r")) #freq(c)
	cc_freq_d = pickle.load(open(pkl_dir + "mainichi_posid_bigram_counts.pkl","r")) #freq(c_i|c_i-1)
	vc_freq_d = pickle.load(open(pkl_dir + "mainichi_posid_word_counts.pkl","r")) #freq(v|c)

	#for pos, v_dict in vc_freq_d.items():
	#	for v, freq in v_dict.items():
	#		print pos, v, freq

	#for pos, freq in c_freq_d.items():
	#	print pos, freq

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

	#Eステップで更新する頻度の初期化　freq_e
	freq_e = Freq(defaultdict(int), defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(int))

	#2.初期頻度_dから確率値の計算をし、コスト（対数）に変換
	cc_cost_e = freq_d.calc_cost("cc", 10)
	vc_cost_e = freq_d.calc_cost("vc", 10)
	wv_cost_e = freq_d.calc_cost("wv", 10)

	#Costオブジェクトに格納
	cost_dict = Cost(cc_cost_e, vc_cost_e, wv_cost_e)

	#------------------初期値でのデコード例----------------------------------
"""
	#文の入力
	#input_sent = raw_input('input a sentence\n')
	input_sent = "ごはんをたべる。"

	#ラティスの生成
	lm = Lattice_Maker(cost_dict.vc, read_pron_dic, cost_dict.wv, cost_dict.cc, id_def)
	lattice = lm.create_lattice(input_sent)
	#pickle.dump(lattice, open(pkl_dir + "lattice_gohanwotaberu.pkl","w"))

	#ビタビによる最適な系列の決定
	best_sequence = lm.viterbi(lattice)

	#最適系列の出力
	lm.show_best_sequence(best_sequence)
	
	#最適系列から得られた頻度
	increase_counts = lm.return_best_sequence_counts(best_sequence)


	#コストの更新
	print increase_counts.show_info()
	[cost_dict, freq_e] = update_cost_freq(cost_dict, freq_e, freq_d, increase_counts)
	cost_dict.show_info()
"""
	#-----------------------------------------------------------------------

	#-------------------学習----------------------------------------
	
	#ファイルの入力
	input_file = open(sys.argv[1]) 

	for input_sent in input_file:
		#updateされたコストをモデルに組み込む
		lm = Lattice_Maker(cost_dict, read_pron_dic, id_def)
		#ラティスの生成
		lattice = lm.create_lattice(input_sent)
		#ビタビによる最適な系列の決定
		best_sequence = lm.viterbi(lattice)
		#最適系列の出力
		lm.show_best_sequence(best_sequence)
		#最適系列から得られた頻度
		increase_counts = lm.return_best_sequence_counts(best_sequence)
		#コストのアップデート
		[cost_dict, freq_e] = update_cost_freq(cost_dict, freq_e, freq_d, increase_counts)









if __name__ == '__main__':
	main()