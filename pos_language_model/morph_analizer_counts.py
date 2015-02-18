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
	prob_ab = (alpha * f_ba_e + beta * f_ba_d) / float(alpha * sigma_a_e + beta * sigma_a_d)
	return prob_ab



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

def update_cost_freq(cost_dict, freq_e, freq_d, increase_counts):
	"""
	input : Eステップで得られた頻度 , 初期値の頻度, 更新差分
	output : 各コストの辞書 vc_cost, wv_cost, cc_cost
	"""
	#vc, cc の頻度update
	for posid_pair, count in increase_counts.cc.items():
		#posid_pair = (pre_posid, next_posid)
		freq_e.cc[posid_pair[0]][posid_pair[1]] = freq_e.cc[posid_pair[0]].get(posid_pair[1], 0) + count
		
	for vc_pair, count in increase_counts.vc.items():
		#vc_pair = (c, v)
		freq_e.vc[vc_pair[0]][vc_pair[1]] = freq_e.vc[vc_pair[0]].get(vc_pair[1], 0) + count

	for wv_pair, count in increase_counts.wv.items():
		freq_e.wv[wv_pair[0]][wv_pair[1]] = freq_e.wv[wv_pair[0]].get(wv_pair[1], 0) + count

	#c の頻度update と同時にコストもアップデート
	#c_freq の更新
	for pos, count in increase_counts.c.items():
		freq_e.c[pos] += count
		
		#cc_cost の更新	#cost(c2|c1) についてc2を全てなめて更新
		for next_pos in cost_dict.cc[pos].keys():
			cost_dict.cc[pos][next_pos] = - math.log(count_mergin(freq_e.cc[pos].get(next_pos,0), freq_d.cc[pos].get(next_pos,0), freq_e.c[pos], freq_d.c[pos], 0.01))
		#vc_cost の更新	#cost(v|c) についてvを全てなめて更新
		#for v_word in cost_dict.vc[pos].keys():
		#	update_cost = = - math.log(count_mergin(freq_e.vc[pos].get(v_word,0), freq_d.vc[pos].get(v_word,0), freq_e.c[pos], freq_d.c[pos], 0.01))
		#	cost_dict.vc[pos][v_word] 

	#cc_cost の更新	#increase_counts(c2|c1) についてc2を全てなめて更新
	for pair_pos in increase_counts.cc.keys(): 
		pos = pair_pos[0]
		next_pos = pair_pos[1]
		cost_dict.cc[pos][next_pos] = - math.log(count_mergin(freq_e.cc[pos].get(next_pos,0), freq_d.cc[pos].get(next_pos,0), freq_e.c[pos], freq_d.c[pos], 0.01))

	#vc_cost の更新	#increase_counts(v|c) についてvを全てなめて更新
	#for pair_vc in increase_counts.vc.keys(): 
	#	pos = pair_vc[0]
	#	word = pair_vc[1]
	#	cost_dict.vc[pos][word] = - math.log(count_mergin(freq_e.vc[pos].get(word,0), freq_d.vc[pos].get(word,0), freq_e.c[pos], freq_d.c[pos], 0.01))

	#vc_costの更新 {surface1:[morph11, morph12,.....],  surface2:[morph21, morph22,....],... }, Morph (surface, posid, vc_cost) 
	#上記のような構造になっているので全て再計算し直さなければならない
	new_vc_cost = defaultdict(list)
	for posid, word_freq_e_dict in freq_e.vc.items():
		for word, count in word_freq_e_dict.items():
			cost = - math.log(count_mergin(count, freq_d.vc[posid].get(word,0), freq_e.c[posid], freq_d.c[posid], 0.01))
			new_vc_cost[word].append(Morph(word, posid, posid, cost))

	for posid, word_freq_d_dict in freq_d.vc.items():
		for word, count in word_freq_d_dict.items():
			cost = - math.log(count_mergin(freq_d.vc[posid].get(word,0), count, freq_e.c[posid], freq_d.c[posid], 0.01))
			new_vc_cost[word].append(Morph(word, posid, posid, cost))

	#v_freqの更新
	for v_word, count in increase_counts.v.items():
		freq_e.v[v_word] += count
		#cost(w|v)のvがかかるコストを全てなめて更新
		for w_word in cost_dict.wv[v_word].keys(): #cost(w|v)のvがかかるコストを全てなめて更新
			cost_dict.wv[v_word][w_word] = - math.log(freq_e.wv[v_word][w_word]  / float(freq_e.v[v_word]), 10)

	for pair_wv in increase_counts.wv.keys(): 
		v_word = pair_wv[0]
		w_word = pair_wv[1]
		#print "v,w : ",  pair_wv
		#print "v,w : ", freq_e.wv[v_word][w_word], "v : ", freq_e.v[v_word]
		cost_dict.wv[v_word][w_word] = - math.log(freq_e.wv[v_word][w_word]  / float(freq_e.v[v_word]), 10)

	return [cost_dict, freq_e]




class Cost():
	"""
	ラティス展開、コスト計算に必要な辞書を要素としてもつ
	"""
	def __init__(self, cc_cost, vc_cost, wv_cost):
		self.cc = cc_cost
		self.vc = vc_cost
		self.wv = wv_cost

	def show_info(self):
		print "cc_cost", self.cc
		print "vc_cost", self.vc
		print "wv_cost", self.wv


class Counts():
	"""
	現在のパラメータから得られた最適な系列で得られた頻度を格納したクラス
	c_counts["posid"], c_counts[(pre_posid, posid)], vc_counts[(c, v)], v_counts[v], wv_counts[(v, w)]
	"""
	def __init__(self, c_counts, cc_counts, vc_counts, v_counts, wv_counts):
		self.c = c_counts
		self.cc = cc_counts
		self.vc = vc_counts
		self.v = v_counts
		self.wv = wv_counts

	def show_info(self):
		print "c_count", self.c
		print "cc_count", self.cc
		print "vc_count", self.vc 
		print "v_count", self.v
		print "wv_count", self.wv

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

	def update_counts(self, increase_counts):
		#c_freq の更新
		for pos, count in increase_counts.c.items():
			self.c[pos] += count

		#v_freqの更新
		for word, count in increase_counts.v.items():
			self.v[word] += count

		for posid_pair, count in increase_counts.cc.items():
			#posid_pair = (pre_posid, next_posid)
			self.cc[posid_pair[0]][posid_pair[1]] = self.cc[posid_pair[0]].get(posid_pair[1], 0) + count
		
		for vc_pair, count in increase_counts.vc.items():
			#vc_pair = (c, v)
			self.vc[vc_pair[0]][vc_pair[1]] = self.vc[vc_pair[0]].get(vc_pair[1], 0) + count

		for wv_pair, count in increase_counts.wv.items():
			self.wv[wv_pair[0]][wv_pair[1]] = self.wv[wv_pair[0]].get(wv_pair[1], 0) + count


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
	def __init__(self, cost_dict, rpdic, iddef):
		self.wdic = cost_dict.vc
		self.wvcos = cost_dict.wv
		self.cccos = cost_dict.cc
		self.rpdic = rpdic
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
							pos_cost = self.cccos[pre_pos].get(pos, 100) #キーエラーを回避するために例がないものには高いコストを与える
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
		vc_counts = defaultdict(int)
		v_counts = defaultdict(int)

		pre_posid = None

		for best_node in best_sequence:
			[v, w, posid] = best_node.return_info()
			posid_unigram_counts[posid] += 1
			posid_word_counts[(posid, v)] += 1
			v_counts[v] += 1
			wv_counts[(v, w)] += 1
			
			if pre_posid:
				posid_bigram_counts[(pre_posid,posid)] += 1
				pre_posid = posid
			else:
				pre_posid = posid

		return Counts(posid_unigram_counts, posid_bigram_counts, posid_word_counts, v_counts, wv_counts)















