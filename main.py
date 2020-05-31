import tkinter as tk
from tkinter import ttk
import sqlite3



class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        ttk_style = ttk.Style()

        self.account_frame = ttk.Labelframe(toolbar, text=f'Баланс')
        self.account_frame.grid_propagate(0)
        self.account_frame.pack(side=tk.LEFT)
        ##TODO растянуть по высоте
        account_balance = f"{account.cur_balance}"
        self.account_label = tk.Label(self.account_frame, text="Баланс:")
        self.account_label.grid(column=0, row=0)

        self.account_balance = tk.Label(self.account_frame, text=account_balance, font="Arial 20")
        self.account_balance.grid(column=1, row=0)
        accounts_name_list = [ _acc_name for _acc_id, _acc_name, _acc_bal in db.get_accounts_list() ]
        self.accounts_list = ttk.Combobox(self.account_frame, values=accounts_name_list)
        self.accounts_list.state(['readonly'])
        self.accounts_list.grid(column=0, row=1, columnspan=2)
        self.accounts_list.current(0)  ## define current

        self.account_label.pack()
        self.account_balance.pack()
        self.accounts_list.pack()


        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить\nпозицию', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img, width=70, wraplength=70)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog, width=70, wraplength=70)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records, width=70, wraplength=70)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.gif')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog, width=70, wraplength=70)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records, width=70, wraplength=70)
        btn_refresh.pack(side=tk.LEFT)
        #self.account_frame.configure(height=180)  #TODO: dirty yugly hack for fit label to height


        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'type', 'total'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('type', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('type', text='Статья дохода/расхода')
        self.tree.heading('total', text='Сумма')

        self.tree.pack()

    def records(self, description, op_type, total):
        self.db.insert_data(description, op_type, total)
        self.view_records()

    def update_record(self, description, op_type, total):
        self.db.c.execute('''UPDATE oper_log SET description=?, type=?, total=? WHERE ID=?''',
                          (description, op_type, total, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        account.recount()
        self.db.c.execute('''SELECT oper_log.id, oper_log.description,  oper_log.type, oper_log.total 
        FROM oper_log 
        JOIN accounts ON accounts.id=oper_log.acc_id and accounts.id= ? ; ''', (account.id,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]
        account_balance = f"{account.cur_balance}"
        self.account_balance.configure(text=account_balance)

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM oper_log WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute('''SELECT description, type, total FROM oper_log WHERE description LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить доходы/расходы')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Статья дохода/расхода:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сумма:')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_money.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_money.get()))

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT id, description, type, total FROM oper_log WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        print(row)
        self.entry_description.insert(0, row[1])
        if row[2] != 'Доход':
            self.combobox.current(1)
        self.entry_money.insert(0, row[3])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.c = self.conn.cursor()
        self.c.executescript('''
        CREATE TABLE IF NOT EXISTS `accounts` (
            `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `name`	TEXT,
            `description`	TEXT,
            `cur_balance`	NUMERIC,
            `refresh_dt`	DATETIME,
            `currency`	TEXT
        );
        CREATE TABLE IF NOT EXISTS `oper_log` (
            `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `timestamp`	DATETIME,
            `description`	TEXT,
            `total`	NUMERIC,
            `type`	TEXT,
            `acc_id`	INTEGER
        );
        ''')
        self.c.execute('''select count(1) from `accounts`;''')
        cnt = self.c.fetchone()[0]
        if cnt == 0:
            self.c.execute(
                '''INSERT INTO `accounts` (name, description, cur_balance, refresh_dt, currency) VALUES (?,?,?,?,?);''',
                ('Наличные', 'счет по-умолчанию', 0, 0, 'USD'))
        self.conn.commit()

    def insert_data(self, description, op_type, total):
        self.c.execute('''INSERT INTO oper_log(description, type, total, acc_id) VALUES (?, ?, ?, ?)''',
                       (description, op_type, total, account.id))
        self.conn.commit()

    def get_account_by_id(self, account_id=None):
        if account_id is None:
            # get default acc. it account with min id
            self.c.execute('''SELECT id, name, cur_balance FROM ACCOUNTS ORDER BY id LIMIT 1''')
        else:
            self.c.execute('''SELECT id, name, cur_balance FROM ACCOUNTS where id = ? ''', (account_id,))

        (account_id, name, cur_balance) = self.c.fetchone()
        return account_id, name, cur_balance

    def get_accounts_list(self):
        self.c.execute('''SELECT id, name, cur_balance FROM ACCOUNTS''')
        accounts_list = self.c.fetchall()  # [ (account_id, name, cur_balance) ]
        return accounts_list

    def recount_by_account_id(self, account_id=None):
        if account_id is None:
            raise RuntimeError('Error: recount_by_account_id with empty account_id')
        self.c.execute('''SELECT total, type FROM oper_log WHERE acc_id = ?''', (account_id,))

        target_balance = 0.0
        for total, op_type in self.c.fetchall():
            if op_type == 'Доход':
                target_balance = round(target_balance + total, 2)
            else:  # op_type == 'Расход':
                target_balance = round(target_balance - total, 2)
        self.c.execute('''UPDATE accounts SET cur_balance = ? WHERE id = ?''', (target_balance, account_id))
        self.conn.commit()


class Account:
    # emtpy values. just in case
    id = 0
    name = ""
    cur_balance = -1

    def __init__(self):
        (self.id, self.name, self.cur_balance) = db.get_account_by_id()

    def recount(self):
        db.recount_by_account_id(self.id)
        ## повторное использование метода, с целью получить значение лишь одного поля.
        (self.id, self.name, self.cur_balance) = db.get_account_by_id(self.id)
        pass

    #TODO добавить возможность управлениям счетами:
    #TODO   создание новых, удаление, просмотр/выбор текущего. возможно добавить метку текущего счета.


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    account = Account()
    app = Main(root)
    app.pack()
    root.title("Household finance")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()
