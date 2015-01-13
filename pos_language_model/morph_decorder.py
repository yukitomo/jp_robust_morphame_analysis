#!/usr/bin/python
#-*-coding:utf-8-*-
#2015-01-07 Yuki Tomo

import pickle
from morph_analyzer_v2 import load_2colums,load_3colums_number, Lattice_Node
from collections import defaultdict


class Node_result():
	def __init__(self, node, begin_idx, end_idx, best_score, best_edge):
		self.node = node
		self.b_idx = begin_idx
		self.e_idx = end_idx
 		self.score = best_score
		self.edge = best_edge

	def showinfo(self):
		print "[b_index, e_index, best_score, best_edge] = [%d, %d, %f, (%d, %d)]"%(self.b_idx, self.e_idx, self.score, self.edge[0], self.edge[1])
		self.node.showinfo()

	def showinfo_pos(self,iddef):
		print "[b_index, e_index, best_score, best_edge] = [%d, %d, %f, (%d, %d)]"%(self.b_idx, self.e_idx, self.score, self.edge[0], self.edge[1])
		self.node.showinfo()
		print iddef[self.node.id_l]

def viterbi(lattice,cccos,iddef):
	sent_length = len(lattice)
	lattice_result = defaultdict(list)
	BOS_node = Node_result(lattice[0][1][0], 0, 1, 0, (-1,0))
	#EOS_node = Node_result(lattice[sent_length-1][sent_length][0], sent_length-1, sent_length, 0, (0,0))
	lattice_result[1].append(BOS_node)
	#lattice_result[9].append(EOS_node)
	#print lattice_result

	#Forward
	for b_i, v in lattice.items():
		if b_i > 0:
			for e_i, node_list in v.items():
				print "forcus index"
				print "[b_i, e_i] = [%d, %d]"%(b_i, e_i)

				for node in node_list:
					pos = node.id_l
					gen_cost = node.vc_cost + node.wv_cost
					best_score = 1000000000
					print "forcus node"
					node.showinfo()
				
					#見ているノードの手前のノードからベストスコアとなるノードのindexをベストエッジとする
					i = 0
					print "pre_node"
					for pre_node in lattice_result[b_i]:
						pre_node.showinfo()
						pre_pos = pre_node.node.id_l
						pos_cost = cccos[pre_pos][pos]
						cand_score = pre_node.score + pos_cost + gen_cost
						print cand_score

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

	for best_node in best_sequence:
		best_node.showinfo_pos(iddef)
		






def main():
	"""
	ラティスから最適パスを決定する
	"""
	pkl_dict = "/Users/yukitomo/Research/jp_robust_morphame_analysis/pkl_data/" 
	dict_dir = "/Users/yukitomo/Research/jp_robust_morphame_analysis/data/mecab-ipadic-2.7.0-20070801-utf8/"
	iddef = load_2colums(open(dict_dir + "left-id.def","r")," ") #mecabはr,l同じID
	lattice = pickle.load(open(pkl_dict + "lattice_gohanwotaberu.pkl","r"))
	cccos = load_3colums_number(open(dict_dir + "matrix.def","r"), " ")
	

	viterbi(lattice, cccos, iddef)



if __name__ == '__main__':
	main()