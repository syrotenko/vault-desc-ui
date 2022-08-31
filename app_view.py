import tkinter as tk
from tkinter import ttk
from app_view_model import ConnectMethod


class AppView(tk.Tk):
    TITLE = 'vault-desk-ui'
    GEOMETRY = '650x500'

    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel
        self.title(self.TITLE)
        self.geometry(self.GEOMETRY)

        self.server_var = None
        self.connect_method_var = None
        self.token_var = None
        self.ldap_user_var = None
        self.ldap_pass_var = None
        self.folders = None
        self.root_v_node = None
        self.vault_data = None

        self.create_ui()

        self.root_v_node = self.viewmodel.get_first_node()
        self.init_vault_data_tree(self.root_v_node)

    def create_ui(self):
        connect_view = self.create_connect_view()
        connect_view.grid(column=0, row=0)
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(column=0, row=1, sticky=tk.EW, pady=5)
        vault_data_view = self.create_vault_data_view()
        vault_data_view.grid(column=0, row=2)

    def create_connect_view(self):
        canvas = tk.Canvas(self, highlightthickness=0)
        tk.Label(canvas, text='Server:').grid(column=1, row=0)

        self.server_var = tk.StringVar(canvas, self.viewmodel.server)
        server_input = tk.Entry(canvas, textvariable=self.server_var)
        server_input.grid(column=2, row=0, sticky=tk.EW)

        self.connect_method_var = tk.StringVar(canvas, self.viewmodel.connect_method)
        token_rdb = tk.Radiobutton(canvas, variable=self.connect_method_var, value=ConnectMethod.Token)
        token_rdb.grid(column=0, row=1)

        tk.Label(canvas, text='Token:').grid(column=1, row=1)
        self.token_var = tk.StringVar(canvas, self.viewmodel.token)
        token_input = tk.Entry(canvas, show='*', textvariable=self.token_var)
        token_input.grid(column=2, row=1, sticky=tk.EW)

        ldap_rdb = tk.Radiobutton(canvas, variable=self.connect_method_var, value=ConnectMethod.LDAP)
        ldap_rdb.grid(column=3, row=1, rowspan=2, sticky=tk.N)
        tk.Label(canvas, text='LDAP:').grid(column=4, row=1, rowspan=2, sticky=tk.N)
        tk.Label(canvas, text='user:').grid(column=5, row=1, sticky=tk.N)
        self.ldap_user_var = tk.StringVar(canvas, self.viewmodel.ldap_user)
        ldap_user_input = tk.Entry(canvas, textvariable=self.ldap_user_var)
        ldap_user_input.grid(column=6, row=1)

        tk.Label(canvas, text='pass:').grid(column=5, row=2, sticky=tk.N)
        self.ldap_pass_var = tk.StringVar(canvas, self.viewmodel.ldap_pass)
        ldap_pass_input = tk.Entry(canvas, show='*', textvariable=self.ldap_pass_var)
        ldap_pass_input.grid(column=6, row=2)

        connect_btn = tk.Button(canvas, text='Connect', command=self.connect_click)
        connect_btn.grid(column=0, columnspan=6, row=3, sticky=tk.W)
        return canvas

    def connect_click(self):
        self.viewmodel.connect(server=self.server_var.get(), connect_method=self.connect_method_var.get(),
                               token=self.token_var.get(), ldap_user=self.ldap_user_var.get(),
                               ldap_pass=self.ldap_pass_var.get())

    def create_vault_data_view(self):
        canvas = tk.Canvas(self, highlightthickness=0)

        folders_scroll = ttk.Scrollbar(canvas, orient=tk.VERTICAL)
        folders_scroll.grid(column=1, row=0, sticky=tk.NS)

        self.folders = ttk.Treeview(canvas, yscrollcommand=folders_scroll.set)
        self.folders.grid(column=0, row=0, sticky=tk.NSEW)
        folders_scroll.config(command=self.folders.yview)
        self.folders.column("#0", width=150)
        self.folders.bind('<<TreeviewSelect>>', self._on_folder_selected)
        self.folders.bind("<<TreeviewOpen>>", self._on_folders_node_open)

        vault_data_scroll = ttk.Scrollbar(canvas, orient=tk.VERTICAL)
        vault_data_scroll.grid(column=3, row=0, sticky=tk.NS)

        self.vault_data = ttk.Treeview(canvas, yscrollcommand=vault_data_scroll.set)
        self.vault_data.grid(column=2, row=0, sticky=tk.NSEW)
        self.vault_data.config(height=15)
        vault_data_scroll.config(command=self.vault_data.yview)

        self.vault_data['columns'] = ('Key', 'Value')

        self.vault_data.column("#0", width=0, stretch=tk.NO)
        self.vault_data.column("Key", width=200, anchor=tk.CENTER)
        self.vault_data.column("Value", width=200, anchor=tk.CENTER)

        self.vault_data.heading("#0", text="")
        self.vault_data.heading("Key", text="Key", anchor=tk.CENTER)
        self.vault_data.heading("Value", text="Value", anchor=tk.CENTER)

        self.vault_data.bind('<<TreeviewSelect>>', self._on_copy)
        return canvas

    def init_vault_data_tree(self, v_node):
        if not v_node:
            return
        self.folders.insert('', tk.END, text=v_node.name, iid=v_node.get_full_path(), open=False)
        self.populate_vault_node_data(v_node)

    def populate_vault_node_data(self, v_node):
        if not v_node.children:
            return
        for node in v_node.children:
            new_item_id = node.get_full_path()
            if not self.folders.exists(new_item_id):
                self.folders.insert(v_node.get_full_path(), tk.END, text=node.name, iid=new_item_id, open=False)

    def fill_vault_data_table(self, node_path):
        self.vault_data.delete(*self.vault_data.get_children())
        data = self.viewmodel.get_node_data(node_path)
        for k, v in data.items():
            self.vault_data.insert('', tk.END, values=(k, v))

    def _on_folders_node_open(self, event):
        current_item_id = self.folders.focus()
        selected_node = self.root_v_node.get_node(current_item_id)
        if selected_node:
            for child in selected_node.children:
                child.children = self.viewmodel.get_children(child)
                self.populate_vault_node_data(child)

    def _on_folder_selected(self, event):
        node_path = self.folders.focus()
        self.fill_vault_data_table(node_path)

    def _on_copy(self, event):
        item = self.vault_data.selection()
        if item:
            values = self.vault_data.item(item[0], 'values')
