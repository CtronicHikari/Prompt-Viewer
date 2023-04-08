# -*- coding: utf-8 -*- 
import os
import ui

save_path = os.getcwd() + '\\' + 'save_path' + '\\'

root = ui.tool_ui(save_path, title='Prompt Viewer 0.1')

root.ins.mainloop()