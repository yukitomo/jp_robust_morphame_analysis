#!/usr/bin/python
#-*-coding:utf-8-*-
import os,pickle
from collections import defaultdict
from morphological_analyzer import Morph


def file_paths_getter(dir_path, extension):
	"""
	input : ディレクトリのパス、拡張子
	output : 各ファイルのパス
	"""
	extension_length = len(extension)
	for root,dirs,files in os.walk(dir_path):
		#print root,dirs,files
		paths=[]
		for file in files:
			file_address = os.path.join(root, file)
			if file_address[- extension_length :] == extension:
				#print file_address
				paths.append(file_address)
		return paths

def make_dict(dict_file, word_dict, read_pron_dict):
	"""
	input : 各ファイル
	output : word_dict, read_pron_dict
	"""

	for line in dict_file:
		morph_list = line.strip().split(",")
		del morph_list[4:11] #余分な形態素情報を削除
		[surface, posid_l, posid_r, vc_cost, read, pron] = morph_list

		morph = Morph(surface, posid_l, posid_r, vc_cost)
		word_dict[surface].append(morph)
		
		#読み,発音のディクショナリ
		read_pron_dict[read].append(surface)
		if not read == pron:
			read_pron_dict[pron].append(surface)

	return [word_dict, read_pron_dict] 

def main():
	dict_dir = "/Users/yukitomo/Research/jp_robust_morphame_analysis/data/mecab-ipadic-2.7.0-20070801-utf8/"
	dict_file_paths = file_paths_getter(dict_dir, ".csv")

	word_dict = defaultdict(list)
	read_pron_dict = defaultdict(list)

	for f in dict_file_paths:
		print "load : " + f 
		[word_dict, read_pron_dict] = make_dict(open(f,"r"), word_dict, read_pron_dict)

	pickle.dump(word_dict, open("ipadic_word_dict.damp","w"))
	pickle.dump(read_pron_dict, open("ipadic_read_pron_dict.damp","w"))

if __name__ == '__main__':
	main()
