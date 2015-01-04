#!/usr/bin/python
#-*-coding:utf-8-*-
#2014-12-13 Yuki Tomo

"""
ラティス展開
1. 辞書引き(見つからなかったら、音素的に近いものもラティスに加える)
2. ラティスがひらがな化したものの場合、ひらがな化していない場合の二種類を展開
例：くるま
ひらがな化確率がkのときは２つのラティスを展開
くるま（漢字がひらがなになったもの）：k * p(車)
くるま（元々ひらがなのものが変わらなかった場合） : (1-k) * p(くるま)

4. 前向き確率を計算
5. 後ろ向き確率
"""	

import pickle, math, jctconv
from collections import defaultdict

class Morph():
	"""
	単語辞書に格納する形態素
	surface(v),posid(left,right),p(v|c)
	"""
	def __init__(self, surface, id_l, id_r, vc_cost):
		self.surface = surface
		self.posid_l = id_l
		self.posid_r = id_r
		self.cost = vc_cost


class Lattice_Node():
	"""
	ベストパスの計算のために、表記ｗ,　元の表記v , 品詞id, 生成コスト, 変形コスト
	surface(v), posid(left,right),p(v|c),p(w|v) 
	"""
	def __init__(self, v_surface, w_surface, id_l, id_r, vc_cost, wv_cost):
		self.v_surface = v_surface #入力されたものの元の表記v
		self.w_surface = w_surface #入力文字列の表記w
		self.posid_l = id_l #左文脈ID
		self.posid_r = id_r #右文脈ID
		self.vc_cost = vc_cost #品詞cから単語vが生成されるコスト
		self.wv_cost = wv_cost #単語vから表記wが生成されるコスト



def create_lattice(sent,word_dict, read_pron_dict, wv_costs_dict):
	lattice = defaultdict(dict)
	sent = unicode(sent.strip(),"utf-8")

	for i_e in range(len(sent))[1:]: #index_end
		for i_b in range(i_e): #index_begin
			str_part = sent[i_b:i_e] #文字の塊, unicodeをutf-8に変換する必要あり
			lattice[i_b][i_e] = create_nodes(str_part,word_dict, read_pron_dict, wv_costs_dict)
	return lattice


def create_nodes(search_string, word_dict, read_pron_dict, wv_costs_dict):
	"""
	input:検索文字列 w_surface
	output:検索文字列に一致（変化なし）、検索単語から派生（変化あり）した単語のノードリスト

	1. 与えられたstringでサーチし見つかったときは、変換なしコストを付加
	2. 全てひらがなのときはカタカナに変換し検索し、変換コストを付加 
	"""
	nodes_list = []
	#入力の表記wで直接見つかるノードを生成
	nodes_list += [convert_morph2node(morph,search_string, wv_costs_dict) for morph in word_dict[search_string]]
	ex_strings = expand_string(search_string) #入力されたstringを拡張

	for ex_string in ex_strings:
		orig_words = read_pron_dict[ex_string] #読みがex_stringの単語を格納

		for orig_word in orig_words:
			nodes_list += [convert_morph2node(morph,orig_word, wv_costs_dict) for morph in word_dict[orig_word]]

	return nodes_list



def convert_morph2node(morph, w_surface, wv_costs_dict):
	v_surface = morph.surface
	wv_cost = get_wv_cost(w_surface, v_surface, wv_costs_dict)
	node = Lattice_Node(v_surface, w_surface, morph.posid_l, morph.posid_r, morph.vc_cost, wv_cost)
	return node


def get_wv_cost(w_surface, v_surface, wv_costs_dict):
	wv_prob_def = 0.01
	wv_cost_def = math.log(wv_prob_def) 

	if not w_surface == v_surface:
		try: 
			wv_cost = wv_costs_dict[w_surface][v_surface]
		except:
			wv_cost = wv_cost_def
	else:
		wv_cost = math.log(1 - wv_prob_def) 

	return wv_cost



def expand_string(string):
	"""
	input:文字列
	output:拡張された文字列のリスト
	当面はひらがなtoカタカナ
	"""
	ex_strings = []
	
	#ひらがな to カタカナ
	ex_strings.append(jctconv.hira2kata(string))

	return ex_strings


def viterbi_alg(lattice, cc_costs_dict, id_def):
	"""
	input:展開したラティス
	output:最適なパス、v_opt, c_opt
	"""

def load_2colums(input_file,sym):
	load_obj = {}
	for line in input_file:
		line.strip().split(sym) #!/usr/bin/python
		load_obj[line[0]] = line[1]
	return load_obj

def load_3colums(input_file,sym):
	load_obj = defaultdict(dict)
	for line in input_file:
		line.strip().split(sym)
		load_obj[line[0]][line[1]] = line[2]
	return load_obj#!/usr/bin/python


def main():
	dict_dir = "/Users/yukitomo/Research/jp_robust_morphame_analysis/data/mecab-ipadic-2.7.0-20070801-utf8/"

	print "loading dictionary"
	word_dict = pickle.load(open("ipadic_word_dict.pkl", "r"))
	read_pron_dict = pickle.load(open("ipadic_read_pron_dict.pkl", "r"))
	id_def = load_2colums(open(dict_dir + "left-id.def","r")," ") #mecabはr,l同じID

	wv_costs_dict = load_3colums(open(dict_dir + "wv_cost.def","r"),"\t")
	cc_costs_dict = load_3colums(open(dict_dir + "matrix.def","r")," ")

	input_sent = raw_input('input a sentence\n')
	
	lattice = create_lattice(input_sent, word_dict, read_pron_dict, wv_costs_dict)
	print lattice

	#result = viterbi_alg(lattice, cc_costs_dict, id_def)


if __name__ == '__main__':
	main()