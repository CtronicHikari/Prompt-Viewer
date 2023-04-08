# -*- coding: utf-8 -*- 
import json
import os

class str_proc:
    
    def __init__(self):
        pass
    
    def prompt_unpack(self, pack):
        if type(pack) is str:
            data = pack.split('\n')
            if len(data) < 3:
                return False, False, False
            
            data_pos = data[0]
            data_neg = data[1].split('t:')[1].strip()
            tmp_list = data[2].split(',')
            data_pam = ''
            for i in tmp_list:
                data_pam += i.strip() + '\n'
                
            return data_pos, data_neg, data_pam
        elif type(pack) is dict:
            data_pos = pack['Positive prompt']
            data_neg = pack['Negative prompt']
            data_pam = pack['Paramaters']
            
            return data_pos, data_neg, data_pam
        
    
    def prompt_pack(self, pos, neg, pam):
        res = ''
        res += pos
        res += 'Negative prompt: ' + neg
        res += pam.replace('\n', ',')
        return res
    
    def prompt_dic_pack(self, pos, neg, pam):
        res_dict = {}
        res_dict['Positive prompt'] = pos
        res_dict['Negative prompt'] = neg
        res_dict['Paramaters'] = pam
        return res_dict
    
    def json_pack(self, data_dict, save_path, pic_list):
        data_dict['pic_seq'] = pic_list
        json_str = json.dumps(data_dict)
        with open(save_path + 'info.json', 'w') as f:
            f.write(json_str)
            
        return True
    
    def json_unpack(self, save_path):
        file_list = os.listdir(save_path)
        file = ''
        for i in file_list:
            if i == 'info.json':
                file = i
                break
        if file == '':
            return False
        
        file = save_path + file
        
        tmp_dict = {}
        with open(file, 'r') as f:
            json_str = f.read()
            tmp_dict = json.loads(json_str)
        
        data_dict = {}
        pic_list = tmp_dict['pic_seq']
        for i in tmp_dict.keys():
            if i != 'pic_seq':
                data_dict[i] = tmp_dict[i]
            
        return data_dict, pic_list
    
    def unpack_pam(self, data):
        data_list = data.split('\n')
        res_list = []
        for i in data_list:
            res_list.append(i)
        return res_list