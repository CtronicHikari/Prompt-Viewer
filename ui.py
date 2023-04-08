# -*- coding: utf-8 -*- 
import tkinter
import tkinter.messagebox
import tkinter.font
import os
import pyperclip
import windnd
from shutil import copyfile
from ttkbootstrap import Style

import picture
import str_proc

class tool_ui:       
    def __init__(self, save_path, width = 1080, height = 768, offset_x = 400, offset_y = 300, resizable = [False, False], title = 'tool_ui Title'):
        style = Style(theme = 'darkly')        
        self.ins = style.master
        self.ins.geometry(f'{width}x{height}+{offset_x}+{offset_y}')
        self.ins.resizable(resizable[0], resizable[1])
        self.ins.title(title)
        
        self.current = 0
        self.save_path = save_path
        self.data_dict = None
        self.pic_pros = picture.picture_processor(save_path)
        
        self.str_proc = str_proc.str_proc()
        
        
        # 图片控件
        self.btn_pre = tkinter.Button(self.ins, text = '上一张', command = self.btn_pre_click)
        self.btn_next = tkinter.Button(self.ins, text = '下一张', command = self.btn_next_click)
        self.lable_pic = tkinter.Button(self.ins, text = 'test', width = 400, height = 600)
        
        # 文本按钮
        self.btn_copy = tkinter.Button(self.ins, text = '复制Prompt', command = self.copy_prompt)
        self.btn_save = tkinter.Button(self.ins, text = '保存prompt', command = self.save_prompt)
        self.btn_del = tkinter.Button(self.ins, text = '删除prompt', command = self.del_pic)
        self.btn_unpack = tkinter.Button(self.ins, text = ' 提取数据 ', command = self.unpack_prompt)
        self.btn_saveall = tkinter.Button(self.ins, text = '保存至本地', command=self.save_json)
        self.btn_clean = tkinter.Button(self.ins, text = '清空文本', command=self.clean_rich_text)
        
        # 文本控件
        # 标签控件
        self.font = tkinter.font.Font(family='Lucida Grande', size=15)
        self.text_pos = tkinter.Label(self.ins, text='Positive prompt:', justify='left', fg='blue', font=self.font)
        self.text_neg = tkinter.Label(self.ins, text='Negative prompt:', justify='left', fg='red', font=self.font)
        self.text_pam = tkinter.Label(self.ins, text='Parameters:', justify='left', fg='black', font=self.font)
        
        # 文本控件
        self.rich_text_pos = tkinter.Text(self.ins)
        self.rich_text_neg = tkinter.Text(self.ins)
        self.rich_text_pam = tkinter.Text(self.ins)
        self.scrollbar_pos = tkinter.Scrollbar(self.ins)
        self.scrollbar_neg = tkinter.Scrollbar(self.ins)
        self.scrollbar_pam = tkinter.Scrollbar(self.ins)
        
        # 图片控件放置
        self.btn_pre.place(x = 100, y = 680, width = 80, height = 30)
        self.btn_next.place(x = 230, y = 680, width = 80, height = 30)
        self.lable_pic.place(x = 50, y = 50, width = 400, height = 600)
        
        # 文本按钮放置
        self.btn_copy.place(x = 500, y = 680)
        self.btn_save.place(x = 600, y = 680)
        self.btn_unpack.place(x = 700, y = 680)
        self.btn_saveall.place(x = 790, y = 680)
        self.btn_clean.place(x = 900, y = 680)
        self.btn_del.place(x = 970, y = 680)
        
        # 标签控件放置
        self.text_pos.place(x = 500, y = 50)
        self.text_neg.place(x = 500, y = 250)
        self.text_pam.place(x = 500, y = 450)
        
        # 文本控件放置
        self.rich_text_pos.place(x = 500, y = 80, height=150, width=500)
        self.rich_text_neg.place(x = 500, y = 290, height=150, width=500)
        self.rich_text_pam.place(x = 500, y = 490, height=150, width=500)
        self.scrollbar_pos.place(x = 1000, y = 80, height=150, width=15)
        self.scrollbar_neg.place(x = 1000, y = 290, height=150, width=15)
        self.scrollbar_pam.place(x = 1000, y = 490, height=150, width=15)
        
        # 文本控件绑定
        self.scrollbar_pos.config(command=self.rich_text_pos.yview)
        self.rich_text_pos.config(yscrollcommand=self.scrollbar_pos.set)
        
        self.scrollbar_neg.config(command=self.rich_text_neg.yview)
        self.rich_text_neg.config(yscrollcommand=self.scrollbar_neg.set)
        
        self.scrollbar_pam.config(command=self.rich_text_pam.yview)
        self.rich_text_pam.config(yscrollcommand=self.scrollbar_pam.set)
        
        self.ui_init()
        
    def ui_init(self):
        self.data_dict, self.pic_pros.pic = self.str_proc.json_unpack(self.pic_pros.save_path)
        if not self.data_dict:
            tkinter.messagebox.showerror('', 'json解包出错')
        
        if self.pic_pros.count_pic() != len(self.data_dict.keys()):
            tkinter.messagebox.showerror('', '图片数量与info中所记录的数量不符, 可能会出错')
            
        self.changing(0)
        windnd.hook_dropfiles(self.lable_pic, func = self.dragged_pic)

    def changing(self, flag):
        self.change_pic(flag)
        self.change_info()

    def change_info(self):
        pic_file = self.pic_pros.pic[self.current]
        pic_info = self.data_dict[pic_file]
        
        pos, neg, pam = self.str_proc.prompt_unpack(pic_info)
        self.set_pos(pos)
        self.set_neg(neg)
        self.set_pam(pam)

    def change_pic(self, flag):
        new = self.current + flag
        
        if new < 0:
            new = len(self.pic_pros.pic) - 1
        elif new > len(self.pic_pros.pic) - 1:
            new = 0
               
        img, size = self.pic_pros.open_pic(self.pic_pros.pic[new])

        w, h = size
        
        if w > 400:
            h = int(h * 400 / w)
            w = 400
        if h > 600:
            w = int (w * 600 / h)
            h = 600
            
        img = self.pic_pros.image_resize(img, 400, 600)
        
        self.pic_pros.set_current(img)
        self.set_picture_to_lable()
        
        self.current = new
        
    
    def btn_pre_click(self):
        self.changing(-1)
        
    def btn_next_click(self):
        self.changing(1)
        
    def set_picture_to_lable(self):
        image = self.pic_pros.current_pic
        self.lable_pic['image'] = image
        self.lable_pic.image = image
        
    def unpack_prompt(self):
        try:
            prompt_str = self.rich_text_pos.get('0.0', 'end')
            data_pos, data_neg, data_pam = self.str_proc.prompt_unpack(prompt_str)
            if not data_pos:
                tkinter.messagebox.showerror('', '解析错误')
                return
            
            self.set_pos(data_pos)
            self.set_neg(data_neg)
            self.set_pam(data_pam)
        except:
            tkinter.messagebox.showerror('', '解析错误')
            
        
    def copy_prompt(self):
        try:
            pos = self.rich_text_pos.get('0.0', 'end')
            neg = self.rich_text_neg.get('0.0', 'end')
            pam = self.rich_text_pam.get('0.0', 'end')
            
            res = self.str_proc.prompt_pack(pos, neg, pam)
            
            pyperclip.copy(res)
            tkinter.messagebox.showinfo('', '已复制参数, 可粘贴到Stable Diffusion中')
        except:
            tkinter.messagebox.showerror('', '复制错误')
        
    def save_prompt(self):
        pos = self.rich_text_pos.get('0.0', 'end')
        neg = self.rich_text_neg.get('0.0', 'end')
        pam = self.rich_text_pam.get('0.0', 'end')
        
        if pos == '' or neg == '' or pam == '':
            tkinter.messagebox.showerror('', '有文本框为空')
            return
        
        res = self.str_proc.prompt_dic_pack(pos, neg, pam)
        self.data_dict[self.pic_pros.pic[self.current]] = res
        if res:
            tkinter.messagebox.showinfo('', '保存Prompt成功')
        
    def dragged_pic(self, file):
        msg = '\n'.join((item.decode('gbk') for item in file))
        
        res = self.check_file(msg.split('\\')[-1])
        
        if res:
            self.data_dict[msg.split('\\')[-1]] = {'Positive prompt':'', 'Negative prompt':'', 'Paramaters': ''}
            self.pic_pros.pic.insert(self.current + 1, msg.split('\\')[-1])
            self.current += 1
            copyfile(msg, self.save_path + msg.split('\\')[-1])
            self.changing(0)
        else:
            for i in range(len(self.pic_pros.pic)):
                if msg.split('\\')[-1] == self.pic_pros.pic[i]:
                    self.changing(i - self.current)
                    self.current = i
            tkinter.messagebox.showinfo('', '存在同名文件')
            
        self.save_json(False)
               
    def del_pic(self):
        key = self.pic_pros.pic[self.current]
        del self.data_dict[key]
        del self.pic_pros.pic[self.current]
        
        self.current -= 1
        if self.current < 0:
            self.current = 0
            self.changing(0)
        else:
            self.changing(-1)
            
        os.remove(self.save_path + key)
        
        self.save_json(False)
            
        
    def check_file(self, file):
        keys = self.data_dict.keys()
        if file in keys:
            return False
        else:
            return True    
    
    def save_json(self, log = True):
        self.str_proc.json_pack(self.data_dict, self.save_path, self.pic_pros.pic)
        if log:
            tkinter.messagebox.showinfo('', '保存至本地成功')
        
    def set_pos(self, data, reset = True):
        if reset:
            self.clean_pos()
        self.rich_text_pos.insert('end', data)
        
    def set_neg(self, data, reset = True):
        if reset:
            self.clean_neg()
        self.rich_text_neg.insert('end', data)
        
    def set_pam(self, data, reset = True):
        if reset:
            self.clean_pam()
        self.rich_text_pam.insert('end', data)
        
    def clean_pos(self):
        self.rich_text_pos.delete('1.0', 'end')
        
    def clean_neg(self):
        self.rich_text_neg.delete('1.0', 'end')
        
    def clean_pam(self):
        self.rich_text_pam.delete('1.0', 'end')
        
    def clean_rich_text(self):
        self.clean_pos()
        self.clean_neg()
        self.clean_pam()

