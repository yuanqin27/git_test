from argparse import Namespace
import json
from collections import defaultdict

args = Namespace(
    # root_path = '/media/zjk/XNH/data/',
    txt_path = "data_filter.txt",
    unique_id_path = "unique_id.txt",
    disease_count_path = "disease_count.txt",
    disease_id_path = "disease_id.txt",

    root_path='/home/yqli/',
)

class DataSet(object):
    def __init__(self, root_path, txt_path, unique_id_path, disease_count_path, disease_id_path, num):
        self.root_path =  root_path
        self.txt_path = root_path + txt_path
        self.unique_id_path = root_path + unique_id_path
        self.disease_count_path = root_path + disease_count_path
        self.disease_id_path = root_path + disease_id_path
        self.num = num

    def count(self, items, cur_dict): # 统计疾病出现的频次
        if isinstance(items, list):
            for item in items:
                cur_dict[item] += 1
        else:
            cur_dict[items] += 1
        return cur_dict

    def gen_count(self):
        disease_count = defaultdict(int)
        with open(self.txt_path, 'r') as fopen, open(self.disease_count_path, 'w') as fout:
            for data in fopen:
                if data != None:
                    data = json.loads(data)
                    disease_count = self.count(data["dname"], disease_count)
            sort_data = sorted(disease_count.items(), key=lambda x: x[1], reverse=True)
            for item in sort_data:
                fout.write(item[0] + "\t" + str(item[1]) + "\n")

    def merge_data(self):
        data_merge_id = defaultdict(list)
        i = 0
        with open(self.txt_path, 'r') as fopen, open(self.unique_id_path, 'w') as fout:
            for line in fopen:
                data = json.loads(line)
                data_merge_id[data['XM']] .append([data['ZYRQ'], data['dname']])
                # i += 1
                # if i % 10000 == 0:
                #     break
            for item in data_merge_id:
                content = json.dumps({item:data_merge_id[item]}, ensure_ascii=False, sort_keys=True)
                fout.write(content)
                fout.write("\n")


    def disease_count_over_number(self): # 出现次数超出num的疾病
        disease_count_over_num = {}
        i = 0
        with open(self.disease_count_path, 'r') as fopen, open(self.disease_id_path, 'w') as fout:
            for line in fopen:
                line = line.replace('\n','').split('\t')
                if int(line[1]) >= self.num:
                    disease_count_over_num[line[0]] = i
                    i += 1
            disease_count_over_num["UNK"] = len(disease_count_over_num)
            for item in disease_count_over_num:
                content = json.dumps({item: disease_count_over_num[item]}, ensure_ascii=False, sort_keys=True)
                fout.write(content)
                fout.write("\n")


data = DataSet(args.root_path, args.txt_path, args.unique_id_path,
               args.disease_count_path, args.disease_id_path,300)
gen_data = data.disease_count_over_number()