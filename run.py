from tkinter import *
import time
from pyecharts.charts import Sankey
from pyecharts import options as opts
from collections import Counter, OrderedDict
"""
github: 
作者: Rumi
打包：pyinstaller --add-data=".\datasets;pyecharts\datasets\." --add-data=".\templates;pyecharts\render\templates\." -F -w *.py
"""
LOG_LINE_NUM = 0

class GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.nodes = Counter()
        self.edges = OrderedDict()
        self.cnt = 0
    
    #设置窗口
    def set_init_window(self):
        self.init_window_name.title('桑基图生成器_v1.0')
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
        self.show_pathes_Text = Listbox(self.init_window_name) #已添加的路径展示
        self.show_pathes_Text.place(x=30, y=280, width=453, height=300)
        self.log_data_Text = Text(self.init_window_name)  # 日志框
        self.log_data_Text.place(x=573, y=95, width=400, height=487)
        #按钮
        self.add_edge_button = Button(self.init_window_name, text='添加路径', bg="lightblue",command=self.add_edge)
        self.add_edge_button.place(x=360, y=50, width=120, height=30)
        self.del_edge_button = Button(self.init_window_name, text='删除上一条路径', bg="lightblue",command=self.del_edge)
        self.del_edge_button.place(x=360, y=100, width=120, height=30)
        self.gen_Sankey_button = Button(self.init_window_name, text='生成桑基图', bg="lightblue",command=self.gen_Sankey)
        self.gen_Sankey_button.place(x=360, y=150, width=120, height=30)

    #功能函数
    def add_edge(self):
        source = self.source_data_Text.get()
        target = self.target_data_Text.get()
        weight = self.weight_data_Text.get()
        self.weight_data_Text.selection_clear()
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
                        self.write_log_to_Text("成功添加1条路径！当前共%s条路径"%(self.cnt)) #需要修改
                else:
                    self.write_log_to_Text("权重必须是正数！")
                # print(self.nodes)
                # print(self.edges)
            except:
                self.write_log_to_Text("权重必须是数字！")
        else:
            self.write_log_to_Text("源节点，目标节点，权重不能为空！")
    
    def del_edge(self):
        #删除上一条路径
        if not self.cnt:
            self.write_log_to_Text("当前没有路径！")
        else:
            s, t = list(self.edges.keys())[-1]
            self.nodes[s] -= 1
            self.nodes[t] -= 1
            del(self.edges[(s, t)])
            self.show_pathes_Text.delete(self.cnt - 1)
            self.cnt -= 1
            self.write_log_to_Text("成功删除当前路径，当前共%s条路径！"%(self.cnt))



    def gen_Sankey(self):
        nodes = list({'name': k} for k in self.nodes.keys())
        linkes = list({'source': s, 'target': t, 'value': w} for (s, t), w in self.edges.items())
        print(nodes)
        print(linkes)
        pic=(
            Sankey().add(
                'Sankey',#图例名称
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
        pic.render('test.html')
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