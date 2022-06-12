import tkinter as tk
import mysql.connector
import hashlib
import json


def erase():
    tran_list.delete(0, tk.END)
    fr2.tkraise()


def records():
    cur.execute(f"SELECT * FROM Transfers "
                f"WHERE Outgoing='{ur.get()}' OR Incoming='{ur.get()}'")
    data = cur.fetchall()
    tran_list.insert(tk.END, ('From', 'Value', 'To'))
    for i in range(len(data)):
        row = [data[i][0], data[i][1] + '$', data[i][2]]
        tran_list.insert(tk.END, row)
        fr4.tkraise()


def transfer():
    try:
        if int(result) < int(val.get()):
            err.set('Insufficient account balance')
        else:
            try:
                cur.execute(f"SELECT Balance FROM Users "
                            f"WHERE User='{to_adr.get()}'")
                up_result = int(cur.fetchall()[0][0]) + int(val.get())

                cur.execute(f"UPDATE Users SET Balance = '{up_result}' WHERE User='{to_adr.get()}'")
                globals()['result'] = int(result) - int(val.get())
                bl_var.set(f'Your balance is: {result}$')
                cur.execute(f"UPDATE Users SET Balance = '{result}' WHERE User='{ur.get()}'")

                cur.execute(f"INSERT INTO Transfers "
                            f"VALUES ('{ur.get()}', '{val.get()}', '{to_adr.get()}')")
                err.set('Successfully transferred')

                val.delete(0, tk.END)
                to_adr.delete(0, tk.END)

                con.commit()
            except IndexError:
                err.set('User not found')
    except ValueError:
        err.set('Incorrect value')


def logout():
    ur.delete(0, tk.END)
    ps.delete(0, tk.END)
    fr1.tkraise()


def register():
    try:
        cur.execute(f"SELECT Balance FROM Users "
                    f"WHERE User='{ur.get()}'")
        cur.fetchall()[0][0]
        if '' != ur.get() and '' != ps.get():
            out_text = 'User currently exist, please change name...'
        else:
            out_text = 'You cannot leave any field empty!'
    except IndexError:
        if '' != ur.get():
            cur.execute(f"INSERT INTO Users "
                        f"VALUES ('{ur.get()}', '{hashlib.sha256(ps.get().encode()).hexdigest()}', '0')")
            out_text = 'Successfully registered, please log in...'
            con.commit()
        else:
            out_text = 'You cannot leave any field empty!'

    lb_var.set(out_text)
    lb3.update()


def login():
    if '' != ur.get() and '' != ps.get():
        try:
            cur.execute(f"SELECT Balance FROM Users "
                        f"WHERE User='{ur.get()}' AND Password='{hashlib.sha256(ps.get().encode()).hexdigest()}'")
            global result
            result = cur.fetchall()[0][0]
            bl_var.set(f'Your balance is: {result}$')
            fr2.tkraise()

        except IndexError:
            lb_var.set("Failed to log in, please check the password and the user's name")
            lb3.update()
    else:
        lb_var.set('You cannot leave any field empty!')
        lb3.update()


with open("databaseconfig.json", "r") as f:
    data = json.load(f)
    data = data.get("database-config")[0]
print(data, type(data))

con = mysql.connector.connect(**data)
cur = con.cursor()

window = tk.Tk()
window.title('Bank')

fr1 = tk.Frame(window)
fr2 = tk.Frame(window)
fr3 = tk.Frame(window)
fr4 = tk.Frame(window)

# -----FRAME 1-----
lb1 = tk.Label(fr1, text="User", width=30)
lb1.grid(row=0, column=0)

lb2 = tk.Label(fr1, text="Password")
lb2.grid(row=2, column=0)

lb_var = tk.StringVar()
lb3 = tk.Label(fr1, textvariable=lb_var)
lb3.grid(row=6, column=0)

ur = tk.Entry(fr1)
ur.grid(row=1, column=0)

ps = tk.Entry(fr1)
ps.grid(row=3, column=0)

log = tk.Button(fr1, text="Login", command=login)
log.grid(row=4, column=0)

reg = tk.Button(fr1, text="Register", command=register)
reg.grid(row=5, column=0)

fr1.grid(row=0, column=0, sticky='news')

# -----FRAME 2-----
lb4 = tk.Label(fr2, text=f'Welcome {ur.get()}', width=30)
lb4.grid(row=0, column=0, columnspan=2)

bl_var = tk.StringVar()
lb5 = tk.Label(fr2, textvariable=bl_var)
lb5.grid(row=1, column=0, columnspan=2)

tra = tk.Button(fr2, text='Make a transfer', command=fr3.tkraise)
tra.grid(row=2, column=0)

his = tk.Button(fr2, text='View transfer history', command=records)
his.grid(row=2, column=1)

gap = tk.Label(fr2)
gap.grid(row=3, column=0, columnspan=2)

b_logout = tk.Button(fr2, text='Logout', command=logout)
b_logout.grid(row=4, column=1)

fr2.grid(row=0, column=0, sticky='news')

# -----FRAME 3-----
lb6 = tk.Label(fr3, text='Making a transfer')
lb6.grid(row=0, column=0, columnspan=2)

lb7 = tk.Label(fr3, text='Value: ')
lb7.grid(row=1, column=0)

lb8 = tk.Label(fr3, text='To: ')
lb8.grid(row=2, column=0)

val = tk.Entry(fr3)
val.grid(row=1, column=1)

to_adr = tk.Entry(fr3)
to_adr.grid(row=2, column=1)

err = tk.StringVar()
err_lb = tk.Label(fr3, textvariable=err)
err_lb.grid(row=3, column=0, columnspan=2)

submit_b = tk.Button(fr3, text='Submit', command=transfer)
submit_b.grid(row=4, column=1)

back_1 = tk.Button(fr3, text='Back', command=fr2.tkraise)
back_1.grid(row=5, column=1)
fr3.grid(row=0, column=0, sticky='news')

# -----FRAME 4-----
tran_list = tk.Listbox(fr4)
tran_list.grid(row=0, column=0)

s_bar = tk.Scrollbar(fr4)
s_bar.grid(row=0, column=1)

tran_list.configure(yscrollcommand=s_bar.set)
s_bar.configure(command=tran_list.yview)

back_2 = tk.Button(fr4, text='Back', command=erase)
back_2.grid(row=1, column=1)

fr4.grid(row=0, column=0, sticky='news')


fr1.tkraise()
window.resizable(False, False)
window.mainloop()
