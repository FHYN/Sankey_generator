from tkinter import *
import time
from pyecharts.charts import Sankey
from pyecharts import options as opts
from collections import Counter, OrderedDict
from tkinter.filedialog import *
import json
import os
"""
github: 
作者: Rumi
打包：pyinstaller --add-data=".\datasets;pyecharts\datasets\." --add-data=".\templates;pyecharts\render\templates\." -F -w *.py
"""
# pyinstaller --add-data="D:\Anaconda3\Lib\site-packages\pyecharts\datasets;pyecharts\datasets\." --add-data="D:\Anaconda3\Lib\site-packages\pyecharts\render\templates;pyecharts\render\templates\." -F -w run.py
LOG_LINE_NUM = 0

class GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.nodes = Counter()
        self.edges = OrderedDict()
        self.cnt = 0
        self.dir = ''
    
    #设置窗口
    def set_init_window(self):
        self.init_window_name.title('桑基图生成器_v1.1')
        width = 1068
        height = 689
        screenwidth = self.init_window_name.winfo_screenwidth()
        screenheight = self.init_window_name.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
        self.init_window_name.geometry(alignstr)
        #标签，Label，可以输入文本
        self.source_data_label = Label(self.init_window_name, text="源节点：", font=(8))
        self.target_data_label = Label(self.init_window_name, text="目标节点：", font=(8))
        self.weight_data_label = Label(self.init_window_name, text="权重：", font=(8))
        self.show_pathes_label = Label(self.init_window_name, text="已经添加的路径：", font=(8))
        self.log_label = Label(self.init_window_name, text="日志：", font=(8))
        self.source_data_label.place(x=30, y=50) #调整Label在UI中的的位置
        self.target_data_label.place(x=30, y=100)
        self.weight_data_label.place(x=30, y=150)
        self.show_pathes_label.place(x=30, y=245)
        self.log_label.place(x=568, y=50)
        #文本框
        self.source_data_Text = Entry(self.init_window_name)  #源节点：self.source_data_Text
        self.source_data_Text.place(x=160, y=50, width=120, height=28)
        self.target_data_Text = Entry(self.init_window_name)  #目标节点：self.target_data_Text
        self.target_data_Text.place(x=160, y=100, width=120, height=28)
        self.weight_data_Text = Entry(self.init_window_name)  #权重：self.weight_data_Text
        self.weight_data_Text.place(x=160, y=150, width=120, height=28)     
        self.show_pathes_Text = Listbox(self.init_window_name) #已添加的路径展示，可以选中修改权重
        self.show_pathes_Text.place(x=30, y=280, width=453, height=300)
        self.log_data_Text = Text(self.init_window_name)  # 日志框
        self.log_data_Text.place(x=573, y=95, width=400, height=487)
        #按钮
        self.add_edge_button = Button(self.init_window_name, text='添加路径', bg="lightblue",command=self.add_edge)
        self.add_edge_button.place(x=360, y=50, width=120, height=30)
        self.del_edge_button = Button(self.init_window_name, text='删除选中的路径', bg="lightblue",command=self.del_edge)
        self.del_edge_button.place(x=360, y=100, width=120, height=30)
        self.gen_Sankey_button = Button(self.init_window_name, text='生成桑基图', bg="lightblue",command=self.gen_Sankey)
        self.gen_Sankey_button.place(x=360, y=150, width=120, height=30)
        #菜单栏
        menubar = Menu(self.init_window_name)
        fmenu1 = Menu(menubar, tearoff=False)
        fmenu1.add_command(label='保存数据', command=self.save_data)
        fmenu1.add_command(label="加载数据", command=self.load_data)
        menubar.add_cascade(label="文件", menu=fmenu1)
        self.init_window_name.config(menu=menubar)

    #功能函数
    def add_edge(self):
        source = self.source_data_Text.get()
        target = self.target_data_Text.get()
        weight = self.weight_data_Text.get()
        if source == target:
            self.write_log_to_Text("源节点与目标节点不可以相同！") #需要修改
        elif source and target and weight:
            try:
                weight = float(weight)
                if weight > 0:
                    self.nodes[source] += 1
                    self.nodes[target] += 1
                    tup = (source, target)
                    if tup in self.edges.keys() or (target, source) in self.edges.keys():
                        self.write_log_to_Text("当前路径已经被添加过")
                    else:
                        self.edges[tup] = weight
                        self.show_pathes_Text.insert(self.cnt,'%s——>%s  权重：%s\n'%(source, target, weight))
                        self.cnt += 1
                        self.write_log_to_Text("成功添加1条路径，当前共%s条路径！"%(self.cnt)) #需要修改
                        self.source_data_Text.delete(0, len(source))
                        self.target_data_Text.delete(0, len(target))
                        self.weight_data_Text.delete(0, len(str(weight)))
                else:
                    self.write_log_to_Text("权重必须是正数！")
                # print(self.nodes)
                # print(self.edges)
            except:
                self.write_log_to_Text("权重必须是数字！")
        else:
            self.write_log_to_Text("源节点，目标节点，权重不能为空！")
    
    def del_edge(self):
        #删除当前选中的路径
        if not self.cnt:
            self.write_log_to_Text("当前没有路径！")
        else:
            try:
                idc = self.show_pathes_Text.curselection()[0]
                s, t = list(self.edges.keys())[idc]
                self.nodes[s] -= 1
                self.nodes[t] -= 1
                if self.nodes[s] <= 0:
                    del(self.nodes[s])
                if self.nodes[t] <= 0:
                    del(self.nodes[t])
                self.source_data_Text.insert(0, s)
                self.target_data_Text.insert(0, t)
                self.weight_data_Text.insert(0, str(self.edges[(s, t)]))
                del(self.edges[(s, t)])
                self.show_pathes_Text.delete(idc, idc)
                self.cnt -= 1
                self.write_log_to_Text("成功删除当前路径，当前共%s条路径！"%(self.cnt))
            except:
                self.write_log_to_Text("请选择一条待删除的路径！")

    def save_data(self):
        filepath = asksaveasfilename(defaultextension='.json', filetypes=[("JSON", "json")], initialdir=os.getcwd(), title='保存')
        edges = [[s, t, w] for (s, t), w in self.edges.items()]
        dic = {'nodes': self.nodes, 'edges': edges}
        dic = json.dumps(dic)
        with open(filepath, 'w') as f:
            json.dump(dic, f)
        f.close()
        self.write_log_to_Text("成功保存当前路径至文件：%s"%(filepath))
        return filepath.split('/')[-1][:-5]


    def load_data(self):
        filepath = askopenfilename(initialdir=os.getcwd(), filetypes=[("JSON", "json")], title='加载')
        if filepath.endswith('.json'):
            with open(filepath, 'r') as f:
                dic = json.load(f)
                dic = json.loads(dic)
                print(dic)
                print(type(dic))
                self.nodes = dic['nodes']
                edges = dic['edges']
            f.close()
            self.edges = OrderedDict()
            self.show_pathes_Text.delete(0, self.cnt)
            for i, (s, t, w) in enumerate(edges):
                self.show_pathes_Text.insert(i, '%s——>%s  权重：%s\n'%(s, t, w))
                self.edges[(s, t)] = w
            self.cnt = len(edges)        
            self.write_log_to_Text("成功加载文件，当前共%s条路径！"%(self.cnt))
        else:
            root1 = Tk()
            root1.title('错误！')
            Label(root1,text='请选择.json文件！',fg='red',width=20, height=6).pack()
            Button(root1,text='确定',width=3,height=1,command=root1.destroy).pack(side='bottom')
            screenwidth = root1.winfo_screenwidth()
            screenheight = root1.winfo_screenheight()
            width = 300
            height = 160
            alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
            # print(screenheight, screenwidth)
            root1.geometry(alignstr)
        

    def gen_Sankey(self):
        nodes = list({'name': k} for k in self.nodes.keys())
        linkes = list({'source': s, 'target': t, 'value': w} for (s, t), w in self.edges.items())
        if not (nodes and linkes):
            self.write_log_to_Text("当前没有任何路径，无法生成桑基图！")
        else:     
            filename = self.save_data()
            # print(nodes)
            # print(linkes)
            pic=(
                Sankey().add(
                    filename,#图例名称
                    nodes,#传入节点数据
                    linkes,#传入边和流量数据
                    #设置透明度、弯曲度、颜色
                    linestyle_opt=opts.LineStyleOpts(opacity=0.3,curve=0.5,color='source'),
                    #标签显示位置
                    label_opts=opts.LabelOpts(position='right'),
                    #节点之间的距离
                    node_gap=30,
                )
                .set_global_opts(title_opts=opts.TitleOpts(title='桑基图'))
            )
            pic.render('%s.html'%(filename))
            self.write_log_to_Text("成功生成桑基图！")
    
    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time
    
    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 28:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)
    
def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()