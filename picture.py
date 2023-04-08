# -*- coding: utf-8 -*- 
import os
from PIL import Image, ImageTk

class picture_processor:
    
    def __init__(self, save_path):
        self.pic = [] 
        self.save_path = save_path
        self.current_pic = None
        
    def get_pic(self, save_path, suffix = ('.jpg', '.png', '.jpeg')):
        pic_list = []
        for file in os.listdir(save_path):
            if file.endswith(suffix):
                pic_list.append(file)
        self.pic = pic_list
    
    def count_pic(self):
        return len(self.pic)
    
    def open_pic(self, file):
        image = Image.open(self.save_path + file)
        return image, image.size
        
    def set_current(self, image):
        self.current_pic = ImageTk.PhotoImage(image)

    def image_resize(self, image, screen_width=0, screen_height=0):
        if screen_width <= 0:
            screen_width = 400
        if screen_height <= 0:
            screen_height = 600
        raw_width, raw_height = image.size[0], image.size[1]
        max_width, max_height = raw_width, screen_height        
        min_width = max(raw_width, max_width)
        # 按照比例缩放
        min_height = int(raw_height * min_width / raw_width)
        # 第1次快速调整
        while min_height > screen_height:
            min_height = int(min_height * .9533)
        # 第2次精确微调
        while min_height < screen_height:
            min_height += 1
        # 按照比例缩放
        min_width = int(raw_width * min_height / raw_height)
        # 适应性调整   
        while min_width > screen_width:
            min_width -= 1
        # 按照比例缩放
        min_height = int(raw_height * min_width / raw_width)
        return image.resize((min_width, min_height))
