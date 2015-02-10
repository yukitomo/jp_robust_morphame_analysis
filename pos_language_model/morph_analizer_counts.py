#!/usr/bin/python
#-*-coding:utf-8-*-
#2014-1-21 Yuki Tomo


import pickle, math, jctconv, string
from collections import defaultdict
from make_dict_obj import Morph

def load_2colums(input_file,sym):
	load_obj = {}
	for line in input_file:
		line = line.strip().split(sym) #!/usr/bin/python
		load_obj[int(line[0])] = line[1]
	return load_obj

def load_3colums_string(input_file,sym):
	load_obj = defaultdict(dict)
	for line in input_file:
		line = line.strip().split(sym)
		load_obj[line[0]][line[1]] = line[2]
	return load_obj

def load_3colums_number(input_file,sym):
	load_obj = defaultdict(dict)
	for line in input_file:
		line = line.strip().split(sym)
		if len(line) > 2:
			load_obj[int(line[0])][int(line[1])] = float(line[2])
	return load_obj




def count_mergin(f_ba_e, f_ba_d, sigma_a_e, sigma_a_d, alpha):
	"""
	input : count(b,a)_e, count(b,a)_d, sigma_a_count(b,a)_e, sigma_a_count(b,a)_d, alpha
	output : P(b|a)
	"""
	beta = 1 - alpha
	prob_ab = (alpha * f_ba_e + beta * f_ba_d) / (alpha * sigma_a_e + beta * sigma_a_d)


def parameter_update():
	"""
	input : posid_unigram_freq, posid_bigram_freq, posid_word_freq
	output : wdic, cccos, 
	"""


def calc_cond_prob(single_freq, pair_freq):
	"""
	条件付き確率の計算
	single_freq : unigramの頻度が辞書に格納されたものなど
	pair_freq : bigramの頻度がdict in dict で格納されたものなど pair_freq[previous_word][next_word]
	"""
	cond_prob =defaultdict(dict)
	for previous_element, next_element_dict in pair_freq.items():
		#print "previous_element : %s"%previous_element
		try: #previous_element = "B"を避ける
			previous_element_freq = single_freq[previous_element]
			for next_element, cond_freq in next_element_dict.items():
				#print "next_element : %s"%next_element
				cond_prob[previous_element][next_element] = float(cond_freq) / previous_element_freq
		except: pass
	return cond_prob

def calc_cond_cost(single_freq, pair_freq, base):
	"""
	頻度から確率を計算し、コストを導出
	input:
		single_freq : unigramの頻度が辞書に格納されたものなど
		pair_freq : bigramの頻度がdict in dict で格納されたものなど pair_freq[previous_word][next_word]
		base : logの底

	output:
		- log_base(prob)コスト値（低いほど確率大）
	"""
	cond_cost =defaultdict(dict)
	for previous_element, next_element_dict in pair_freq.items():
		try: #previous_element = "B"を避ける
			previous_element_freq = single_freq[previous_element]
			for next_element, cond_freq in next_element_dict.items():
				cond_cost[previous_element][next_element] = - math.log(float(cond_freq) / previous_element_freq, 10)
		except: pass
	return cond_cost

def calc_cond_cost_vc(single_freq, pair_freq, base):
	"""
	頻度から確率を計算し、コストを導出(vc_costだけ特殊な形)
	#lattice生成のオブジェクトの構造上、morphオブジェクト型に変更する必要あり
	#vc_cost = {surface1:[morph11, morph12,.....], surface2:[morph21, morph22,....],... }
 	#morph_class = [surface, id_l, id_r, vc_cost]

	input:
		single_freq : unigramの頻度が辞書に格納されたものなど
		pair_freq : bigramの頻度がdict in dict で格納されたものなど pair_freq[previous_word][next_word] = freq
		base : logの底

	output:
		- log_base(prob)コスト値（低いほど確率大）
	"""
	cond_cost = defaultdict(list)
	for previous_element, next_element_dict in pair_freq.items(): #品詞, 各単語に対しての頻度辞書
		previous_element_freq = single_freq[previous_element] #品詞の頻度
		for next_element, cond_freq in next_element_dict.items():
			cost = - math.log(float(cond_freq) / previous_element_freq, 10)
			morph = Morph(next_element, previous_element, previous_element, cost)
			cond_cost[next_element].append(morph)
	return cond_cost

class Freq():
	"""
	頻度Freq (d or e) を格納するクラス

	"""
	def __init__(self, c_freq, cc_freq, vc_freq, wv_freq, v_freq):
		self.c = c_freq
		self.cc = cc_freq
		self.vc = vc_freq
		self.wv = wv_freq
		self.v = v_freq

	def calc_prob(self, choice):
		"""
		格納されている各頻度から確率値を計算する(初期の頻度d用)
		output : P(c_i|c_i-1), P(v|c), P(w|v)
		"""
		if choice == "cc":
			return calc_cond_prob(self.c, self.cc)
		elif choice == "vc":
			return calc_cond_prob(self.c, self.vc)
		else :
			return calc_cond_prob(self.v, self.wv)

	def calc_cost(self, choice, base):
		"""
		格納されている各頻度から確率値を計算する(初期の頻度d用)
		base : 対数の底
		output : P(c_i|c_i-1), P(v|c), P(w|v)
		"""
		if choice == "cc":
			return calc_cond_cost(self.c, self.cc, base)
		elif choice == "vc":
			#vc_cost = {surface1:[morph11, morph12,.....], surface2:[morph21, morph22,....],... }
		 	#morph_class = [surface, id_l, id_r, vc_cost]
 			vc_cost = calc_cond_cost_vc(self.c, self.vc, base)
 			return vc_cost
		elif choice == "wv" :
			return calc_cond_cost(self.v, self.wv, base)

		else:
			print "error"



class Prob():
	"""
	各確率を格納 P(c_i|c_i-1), P(v|c), P(w|v)
	"""
	def __init__(cc_prob, vc_prob, wv_prob):
		self.cc = cc_prob
		self.vc = vc_prob
		self.prob = wv_prob


class Lattice_Node():
	"""
	ベストパスの計算のために、表記ｗ,　元の表記v , 品詞id, 生成コスト, 変形コスト
	surface(v), posid(left,right),p(v|c),p(w|v) 
	"""
	def __init__(self, v_surface, w_surface, id_l, id_r, vc_cost, wv_cost):
		self.v_surface = v_surface #入力されたものの元の表記v
		self.w_surface = w_surface #入力文字列の表記w
		self.id_l = int(id_l) #左文脈ID
		self.id_r = int(id_r) #右文脈ID
		self.vc_cost = float(vc_cost) #品詞cから単語vが生成されるコスト
		self.wv_cost = float(wv_cost) #単語vから表記wが生成されるコスト

	def showinfo(self):
		print "[v, w, id_l, id_r, vc_c, wv_c] = [%s, %s, %d, %d, %f, %f]"\
			%(self.v_surface, self.w_surface, self.id_l, self.id_r, self.vc_cost, self.wv_cost)




def expand_string(input_string):
	"""
	input:文字列
	output:拡張された文字列のリスト
	当面はひらがなtoカタカナ
	"""
	ex_strings = []

	#ひらがな to カタカナ
	u_string = unicode(input_string,"utf-8") #unicode化 
	ex_strings.append(jctconv.jctconv.hira2kata(u_string).encode('utf-8'))

	#小文字を含むひらがな to カタカナ (おとぅさん to オトウサン)
	#cap_string = input_string.translate(string.maketrans('ぁぃぅぇぉ', 'あいうえお'))
	#u_cap_string = unicode(cap_string,"utf-8")
	#ex_strings.append(jctconv.jctconv.hira2kata(cap_string).encode('utf-8'))



	#jctconv.normalize(u'ティロ･フィナ〜レ','NFKC')
	"""
	jctconv.normalize
	u'〜' -> u'ー',
	u'～' -> u'ー',
	u"’" -> "'",
	u'”' -> '"',
	u'―' -> '-',
	u'‐' -> '-'
	"""

	#音が近い文字列
	#編集距離

	return ex_strings

class Node_result():
	def __init__(self, node, begin_idx, end_idx, best_score, best_edge):
		self.node = node #Lattice_Node
		self.b_idx = begin_idx
		self.e_idx = end_idx
 		self.score = best_score
		self.edge = best_edge

	def showinfo(self):
		print "[b_index, e_index, best_score, best_edge] = [%d, %d, %f, (%d, %d)]"%(self.b_idx, self.e_idx, self.score, self.edge[0], self.edge[1])
		self.node.showinfo()

	def showinfo_pos(self, iddef):
		print "[b_index, e_index, best_score, best_edge] = [%d, %d, %f, (%d, %d)]"%(self.b_idx, self.e_idx, self.score, self.edge[0], self.edge[1])
		self.node.showinfo()
		print iddef[self.node.id_l]

	def return_info(self):
		"""
		output : パラメータチューニングのために、結果の各要素の頻度を渡す
		[v_surface, w_surface, posid]
		"""
		return [self.node.v_surface, self.node.w_surface, self.node.id_l]



class Lattice_Maker():
	"""
	単語辞書(vc_costも含む)、読み発音辞書、単語変形コスト、品詞遷移コスト
	word_dict, read_pron_dict, wv_costs_dict, cccos
	"""
	def __init__(self, wdic, rpdic, wvcos, cccos, iddef):
		self.wdic = wdic
		self.rpdic = rpdic
		self.wvcos = wvcos
		self.cccos = cccos
		self.iddef = iddef

	def create_lattice(self, sent):
		lattice = defaultdict(dict)
		sent = unicode(sent.strip(),"utf-8")

		for i_e in range(len(sent)+1)[1:]: #index_end
			for i_b in range(i_e): #index_begin
				str_part = sent[i_b:i_e].encode('utf-8') #文字の塊, unicodeをutf-8に変換する必要あり
				lattice[i_b + 1][i_e + 1] = self.create_nodes(str_part)
		#BOS, EOSを付加
		lattice[0][1] = [Lattice_Node("BOS", "BOS", 0, 0, 0, 0)]
		lattice[i_e + 1][i_e + 2] = [Lattice_Node("EOS", "EOS", 0, 0, 0, 0)]

		return lattice

	def create_nodes(self, search_string):
		nodes_list = []
		#入力の表記wで直接見つかるノードを生成
		#nodes_list += [self.convert_morph2node(morph, search_string) for morph in self.wdic[search_string]]
		#print self.wdic[search_string]
		for morph in self.wdic[search_string]:
			#morph.showinfo()
			nodes_list.append(self.convert_morph2node(morph, search_string))

		ex_strings = expand_string(search_string) #入力されたstringを拡張

		for ex_string in ex_strings:
			#print ex_string
			orig_words = self.rpdic[ex_string] #読みがex_stringの単語を格納
			#print orig_words

			for orig_word in orig_words:
				#print orig_word
				#nodes_list += [self.convert_morph2node(morph,orig_word) for morph in self.wdic[orig_word]]
				for morph in self.wdic[orig_word]:
					morph.showinfo()
					nodes_list.append(self.convert_morph2node(morph,search_string))

		return nodes_list
	
	def convert_morph2node(self, morph, w_surface):
		v_surface = morph.surface
		wv_cost = self.get_wv_cost(w_surface, v_surface)
		node = Lattice_Node(v_surface, w_surface, morph.id_l, morph.id_r, morph.vc_cost, wv_cost)
		return node

	def get_wv_cost(self, w_surface, v_surface):
		wv_prob_def = 0.01
		wv_cost_def = - math.log(wv_prob_def) 

		#w,vが異なる文字列のとき変形コストがかかる
		# - math.log(0.01) = 4.605170185988091
		if not w_surface == v_surface:
			try: 
				wv_cost = self.wvcos[w_surface][v_surface]
			except:
				wv_cost = wv_cost_def
		#w,vが同じとき変形しないコストがかかる
		# - math.log(0.99) = 0.01005033585350145
		else:
			wv_cost = - math.log(1 - wv_prob_def) 

		return wv_cost



	def viterbi(self, lattice):
		"""
		input:展開したラティス
		output:最適なパス、v_opt, c_opt
		"""
		sent_length = len(lattice)
		lattice_result = defaultdict(list) #latticeから
		BOS_node = Node_result(lattice[0][1][0], 0, 1, 0, (-1,0))
		lattice_result[1].append(BOS_node)
	
		#Forward
		for b_i, v in lattice.items():
			if b_i > 0:
				for e_i, node_list in v.items():
					#print "forcus index"
					#print "[b_i, e_i] = [%d, %d]"%(b_i, e_i)

					for node in node_list:
						pos = node.id_l
						gen_cost = node.vc_cost + node.wv_cost
						best_score = 1000000000
						#print "forcus node"
						#node.showinfo()
				
						#見ているノードの手前のノードからベストスコアとなるノードのindexをベストエッジとする
						i = 0
						#print "pre_node"
						for pre_node in lattice_result[b_i]:
							#pre_node.showinfo()
							pre_pos = pre_node.node.id_l
							pos_cost = self.cccos[pre_pos][pos]
							cand_score = pre_node.score + pos_cost + gen_cost
							#print cand_score

							if cand_score < best_score:
								best_edge = (b_i , i)
								best_score = cand_score
							i += 1

						node_result = Node_result(node, b_i, e_i, best_score, best_edge)
						lattice_result[e_i].append(node_result)

		#nodeの計算結果の確認
		"""
		for k, v in lattice_result.items():
			for ins in v:
				ins.showinfo()

			print k
		"""

		#Backward 後ろのノードからベストエッジをたどる
		former_edge = (sent_length, 0)
		best_sequence = []

		#former_edge = (-1, 0) にならない限り
		while not former_edge == (-1, 0):
			#print "former_edge", former_edge
			best_node = lattice_result[former_edge[0]][former_edge[1]]
			best_sequence.insert(0,best_node) 
			former_edge = best_node.edge

		"""
		for best_node in best_sequence:
			best_node.showinfo_pos(self.iddef)
		"""
		return best_sequence

	def show_best_sequence(self, best_sequence):
		for best_node in best_sequence:
			best_node.showinfo_pos(self.iddef)

	def return_best_sequence_counts(self, best_sequence):
		posid_unigram_counts = defaultdict(int)
		posid_bigram_counts = defaultdict(int)
		posid_word_counts = defaultdict(int)
		wv_counts = defaultdict(int)

		pre_posid = None

		for best_node in best_sequence:
			[v, w, posid] = best_node.return_info()
			posid_unigram_counts[posid] += 1
			posid_word_counts[(posid, v)] += 1
			wv_counts[(v, w)] += 1

			if pre_posid:
				posid_bigram_counts[(pre_v,v)] += 1

		return [posid_unigram_counts, posid_bigram_counts, posid_word_counts, wv_counts]
