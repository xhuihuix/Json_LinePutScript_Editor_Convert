from tkinter import Tk, Menu, messagebox, Toplevel, Label, Button, NSEW, NS, EW, W, filedialog, Text, END
from tkinter.ttk import Treeview, Scrollbar
from LpsTransFunc import LpsFileToLpsList, LpsListToLpsStr, LpsStrToLpsList, LpsListToJsonStr, JsonStrToLpsList


def load_lps_data():
    global data_map
    data_map = LpsFileToLpsList("vup.lps")

    # 递归添加JSON数据到TreeView
    refresh_json_data(data_map)


def refresh_json_data(data):
    # 清空TreeView
    tree.delete(*tree.get_children())
    for item in data:
        if item == {}:
            continue
        parent_node = tree.insert("", "end", text=item['name'])
        item["node_id"] = parent_node
        tree.set(parent_node, "Value", item['Info'])
        for sub_item_index in item['Sub']:
            child_node = tree.insert(parent_node, "end", text=item['Sub'][sub_item_index]['name'])
            item['Sub'][sub_item_index]["node_id"] = child_node
            tree.set(child_node, "Value", item['Sub'][sub_item_index]['Info'])


def edit_node(event):
    item = tree.focus()
    column = tree.identify_column(event.x)
    if column == '#0':
        node_type = 'Key'
    else:
        node_type = 'Value'

    data_obj = GetItemObj(data_map, item)
    if data_obj is None:
        return
    show_edit_window(item, column, node_type, data_obj)


def add_node():
    item = tree.focus()
    index = tree.index(item)

    data_obj = GetItemObj(data_map, item)
    if data_obj is None:
        return
    if data_obj.get('Sub') is None:
        messagebox.showwarning("警告", "不能在叶子节点添加子节点，请选择非叶子节点")
        return
    show_add_window(item, index, data_obj)


def delete_node():
    item = tree.focus()
    data_obj = GetItemObj(data_map, item)
    if data_obj is None:
        return
    if messagebox.askyesno("警告", "确认删除节点？"):
        tree.delete(item)
        DeleteItemObj(data_map, item)


def GetItemObj(_map, item_id):
    for l1_data in _map:
        if l1_data['node_id'] == item_id:
            return l1_data
        for l2_data in l1_data['Sub']:
            if l1_data['Sub'][l2_data]['node_id'] == item_id:
                return l1_data['Sub'][l2_data]
    return None


def DeleteItemObj(_map, item_id):
    for index, l1_data in enumerate(_map):
        if l1_data['node_id'] == item_id:
            _map.pop(index)
            return
        for index2, l2_data in enumerate(l1_data['Sub']):
            if l1_data['Sub'][l2_data]['node_id'] == item_id:
                l1_data['Sub'].pop(l2_data)
                return


def show_edit_window(item, column, node_type, data_obj):
    edit_window = Toplevel(root) 

    # 获取root窗口的位置
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()

    # 计算弹窗窗口在root窗口中的位置
    x = root_x 
    y = root_y 

    # 设置弹窗窗口的位置
    edit_window.geometry(f"+{x}+{y}")
    label = Label(edit_window, text="当前值：")
    label.grid(row=0, column=0, sticky=W, pady=5)

    # 添加一个Entry控件用于接收修改值
    entry = Text(edit_window, wrap="word")
    entry.insert(1.0, data_obj['Info'] if node_type == "Value" else data_obj['name'])
    entry.grid(row=1, column=0, sticky="ew", padx=5)

    def save_data():
        new_value = entry.get(1.0, END).replace('\n', '')
        # 更新treeview中对应节点的值
        if node_type == "Key":
            tree.item(item, text=new_value)
            data_obj['name'] = new_value
        else:
            tree.set(item, column=column, value=new_value)
            data_obj['Info'] = new_value
        # 关闭弹出框
        edit_window.destroy()

    # 添加一个保存按钮
    save_button = Button(edit_window, text="保存", command=save_data)
    save_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

    # 设置Entry控件的横向宽度与窗口宽度保持一致
    edit_window.grid_columnconfigure(0, weight=1)
    entry.focus()


def show_add_window(item, index, data_obj):
    edit_window = Toplevel(root)  # 添加一个标签用于显示当前选中的值
    # 获取主窗口的宽度和高度
    main_width = root.winfo_width()
    main_height = root.winfo_height()

    # 获取root窗口的位置
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()

    # 计算弹窗窗口在root窗口中的位置
    x = root_x 
    y = root_y 

    # 设置弹窗窗口的位置
    edit_window.geometry(f"+{x}+{y}")

    label = Label(edit_window, text="添加节点名称：")
    label.grid(row=0, column=0, sticky=W, pady=5)

    # 添加一个Entry控件用于接收修改值,长度占满窗口
    entry = Text(edit_window, wrap="word")
    entry.grid(row=1, column=0, sticky="ew", padx=5)

    def save_data():
        # 获取用户输入的修改值
        new_value = entry.get(1.0, END).replace('\n', '')
        # 判断为空
        if new_value == '':
            messagebox.showwarning("警告", "节点名称不能为空")
            return
        # 更新treeview中对应节点的值
        new_node = tree.insert(item, index, text=new_value)
        data_obj['Sub'][new_value] = {'name': new_value, 'Info': '', 'node_id': new_node}

        # 关闭弹出框
        edit_window.destroy()

    # 添加一个保存按钮
    save_button = Button(edit_window, text="保存", command=save_data)
    save_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

    # 设置Entry控件的横向宽度与窗口宽度保持一致
    edit_window.grid_columnconfigure(0, weight=1)
    entry.focus()


def popup(event):
    # 在鼠标位置显示右键菜单
    menu.entryconfigure("修改", command=lambda: edit_node(event))
    menu.entryconfigure("添加", command=lambda: add_node())
    menu.entryconfigure("删除", command=lambda: delete_node())
    menu.post(event.x_root, event.y_root)


def expand_or_collapse_all_nodes():
    global tree
    all_nodes = tree.get_children()
    # 逐个展开节点
    for node in all_nodes:
        obj = tree.item(node)
        if obj['open'] == 0:
            tree.item(node, open=True)
        else:
            tree.item(node, open=False)


def export_lps_file():
    data = LpsListToLpsStr(data_map)
    file_path = filedialog.asksaveasfilename(defaultextension=".lps",
                                             filetypes=[("Lps Files", "*.lps"), ("All Files", "*.*")])
    export_func(file_path, data)


def export_json_file():
    data = LpsListToJsonStr(data_map)
    file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                             filetypes=[("Json Files", "*.json"), ("All Files", "*.*")])
    export_func(file_path, data)


def export_func(file_path, data):
    if file_path:
        try:
            with open(file_path, 'w', encoding="utf-8") as file:
                file.write(data)
            messagebox.showinfo("提示", "文件导出成功！")
        except Exception as e:
            messagebox.showerror("错误", "导出文件时发生错误:" + str(e))
    else:
        print("取消导出文件")


def import_json_file():
    file_path = filedialog.askopenfilename(filetypes=[("Json Files", "*.json"), ("All Files", "*.*")])
    if file_path:
        try:
            global data_map
            with open(file_path, 'r', encoding="utf-8") as file:
                data = file.read()
                # 解析数据
                data_map = JsonStrToLpsList(data)
                # 显示数据
                refresh_json_data(data_map)
            messagebox.showinfo("提示", "文件导入成功！\n 选中节点后，右键菜单可进行修改、添加、删除操作！")
        except Exception as e:
            messagebox.showerror("错误", "导入文件时发生错误:" + str(e))


def input_lps_file():
    file_path = filedialog.askopenfilename(filetypes=[("Lps Files", "*.lps"), ("All Files", "*.*")])
    if file_path:
        try:
            global data_map
            with open(file_path, 'r', encoding="utf-8") as file:
                data = file.read()
                # 解析数据
                data_map = LpsStrToLpsList(data)
                # 显示数据
                refresh_json_data(data_map)
            messagebox.showinfo("提示", "文件导入成功！\n 选中节点后，右键菜单可进行修改、添加、删除操作！")
        except Exception as e:
            messagebox.showerror("错误", "导入文件时发生错误:" + str(e))



root = Tk()
root.geometry("500x700")
root.title("JSON Editor")

tree = Treeview(root, height=20, )
tree.grid(row=0, column=0, columnspan=5, sticky=NSEW)

scrollBar = Scrollbar(root, orient="vertical", command=tree.yview)
scrollBar.grid(row=0, column=5, sticky=NS)

scrollBar = Scrollbar(root, orient="horizontal", command=tree.xview)
scrollBar.grid(row=1, column=0, columnspan=5, sticky=EW)

Button(root, text="读取LPS文件", command=input_lps_file).grid(row=2, column=0)
Button(root, text="读取JSON文件", command=import_json_file).grid(row=2, column=1, )
Button(root, text="导出LPS文件", command=export_lps_file).grid(row=2, column=2, )
Button(root, text="导出JSON文件", command=export_json_file).grid(row=2, column=3, )
Button(root, text="折叠/展开", command=expand_or_collapse_all_nodes).grid(row=2, column=4, )



root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


tree["columns"] = "Value"
tree.column("#0", width=150, minwidth=150)
tree.column("Value", width=150, minwidth=150)
tree.heading("#0", text="Key", anchor="w")
tree.heading("Value", text="Value", anchor="w")

menu = Menu(root, tearoff=0)
menu.add_command(label="修改")
menu.add_command(label="添加")
menu.add_command(label="删除")

tree.bind("<Button-3>", popup)

data_map = []

root.mainloop()
