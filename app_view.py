import tkinter as tk
from tkinter import ttk
from app_view_model import ConnectMethod
from tkinter.constants import *


class AppView(tk.Tk):
    TITLE = 'vault-desk-ui'
    GEOMETRY = '650x400'

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

        self.create_ui()

    def create_ui(self):
        connect_view = self.create_connect_view()
        connect_view.grid(column=0, row=0)
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(column=0, row=1, sticky=tk.EW, pady=5)

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

        folders = ttk.Treeview(canvas)
        folders.grid(column=0, row=0, sticky="nsew")
        folders.column("#0", width=150)

        table_scroll = ttk.Scrollbar(canvas, orient=tk.VERTICAL)
        table_scroll.grid(column=3, row=0, sticky="ns")

        table = ttk.Treeview(canvas, yscrollcommand=table_scroll.set)
        table.grid(column=1, columnspan=2,  row=0, sticky="nsew")
        table.config(height=15)
        table_scroll.config(command=table.yview)

        table['columns'] = ('Key', 'Value')

        table.column("#0", width=0, stretch=NO)
        table.column("Key", width=200, anchor=CENTER)
        table.column("Value", width=200, anchor=CENTER)

        table.heading("#0", text="")
        table.heading("Key", text="Key", anchor=CENTER)
        table.heading("Value", text="Value", anchor=CENTER)
        return canvas
