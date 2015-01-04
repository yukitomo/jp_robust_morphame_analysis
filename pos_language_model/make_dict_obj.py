#!/usr/bin/python
#-*-coding:utf-8-*-
import os,pickle
from collections import defaultdict



"""
単語辞書 : ipadic のインデックスにあるsurfaceに対してマッチする形態素をリストとして持つ
word_dict = {surface1:[morph11, morph12,.....], surface2:[morph21, morph22,....],... }

読み発音辞書 : ipadicにあるインデックスのsurfaceに対しての読み、発音をインデックスとして、元の表記を持つ
read_pron_dict = {rp1:[orig11, orig12,..], rp2:[orig21, orig22,...],... }

"""

class Morph():
	"""
	単語辞書に格納する形態素
	surface(v),posid(left,right),p(v|c)
	"""
	def __init__(self, surface, id_l, id_r, vc_cost):
		self.surface = surface
		self.id_l = int(id_l)
		self.id_r = int(id_r)
		self.vc_cost = float(vc_cost)

	def showinfo(self):
		print "[surface, id_l, id_r, vc_cost] = [%s, %d, %d, %f]"%(self.surface, self.id_r, self.id_l, self.vc_cost)


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
		[surface, id_l, id_r, vc_cost, read, pron] = morph_list

		#print "[surface, id_l, id_r, vc_cost] = [%s, %d, %d, %d]"%(surface, int(posid_l), int(posid_r), int(vc_cost))
		morph = Morph(surface, id_l, id_r, vc_cost)
		morph.showinfo()
		word_dict[surface].append(morph)
		
		#読み,発音のディクショナリ
		read_pron_dict[read].append(surface)
		if not read == pron: #!/usr/bin/python
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

	pickle.dump(word_dict, open("ipadic_word_dict.pkl","w"))
	pickle.dump(read_pron_dict, open("ipadic_read_pron_dict.pkl","w"))

if __name__ == '__main__':
	main()
