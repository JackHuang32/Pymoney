
import pyrecord
import pycategory
import tkinter as tk
from tkinter import messagebox
def add_item(new_record):
    global view_box
    global my_records
    success,new_item,message = my_records.add(new_record)
    if success:
        view_box.insert(view_box.size(),new_item)
        show_money_str.set('Now you have '+str(my_records._money)+' dollars')
        if message:
            messagebox.showwarning(title='Invalid date',message=message)
    else:
        messagebox.showerror(title='Fail to add an record',message=message)
def update_money(mon_str):
    money = 0
    try:
        money = int(mon_str)
    except:
        messagebox.showerror(title='Fail to update money',message='money should be integer!')
        return
    my_records.set_money(money)
    show_money_str.set('Now you have '+str(my_records._money)+' dollars')
    return
def find_record(category):
    success,found_list,total = my_records.find(category)
    if success==2:
        view_box.delete(0,tk.END)
        for i,item in enumerate(found_list):
            view_box.insert(i,item)
        show_money_str.set('The total is '+str(total)+' dollars')   
    elif success == 1:
        messagebox.showinfo(title='Unsuccessful finding',message=found_list)
    elif success == 0:
        messagebox.showerror(title='Unsuccessful finding',message=found_list)
def show_records_back():
    view_box.delete(0,tk.END)
    for i,item in enumerate(my_records.get_items_str()):
        view_box.insert(i,item+'\n')
    show_money_str.set('Now you have '+str(my_records._money)+' dollars')
def delete_selected():
    idx = view_box.curselection()
    if len(idx)==0:#No selection
        return
    del_rec = view_box.get(idx[0])
    delete_record = pyrecord.record(del_rec.split()[0],del_rec.split()[1],del_rec.split()[2],int(del_rec.split()[3]))
    my_records.delete(delete_record)
    view_box.delete(idx[0])
    show_money_str.set('Now you have '+str(my_records._money)+' dollars')
if __name__ == '__main__':
    win = tk.Tk()
    win.title('Pymoney')
    f = tk.Frame(win)
    f.propagate(True)
    f.grid()
    my_categories = pycategory.categories()
    my_records = pyrecord.records()
    #category display
    category_label = tk.Label(f,text='Category',font=('Corier',20))
    category_label.grid(row=0,column=0)
    category_str = ''.join([i for i in my_categories.get_category_str()])
    category_str_label = tk.Label(f,text=category_str,justify=tk.LEFT)
    category_label.propagate(False)
    category_str_label.grid(row=1,column=0)
    #srcollbar for view_box
    scroll = tk.Scrollbar(f,orient=tk.VERTICAL)
    #initial record display
    view_box = tk.Listbox(f,width=40)
    for i,item in enumerate(my_records.get_items_str()):
        view_box.insert(i,item+'\n')
    view_box.grid(row=1,column=1)
    scroll.grid(row=1,column=2,sticky=tk.NS)
    view_box.config(yscrollcommand=scroll.set)
    scroll.config(command=view_box.yview)
    #add record
    add_label = tk.Label(f,text='Add reocrd:',justify=tk.LEFT)
    add_label.grid(row=0,column=3)
    add_str = tk.StringVar()
    add_entry = tk.Entry(f,textvariable=add_str,width=30)
    add_entry.grid(row=0,column=4)
    add_btn = tk.Button(f,text='ADD',command=lambda: add_item(add_str.get()))
    add_btn.grid(row=0,column=5)

    #update money
    update_label = tk.Label(f,text='Update money: ')
    update_label.grid(row=1,column=3)
    money_str = tk.StringVar()
    money_entry = tk.Entry(f,textvariable=money_str)
    money_entry.grid(row=1,column=4)
    update_btn = tk.Button(f,text='Update',command=lambda :update_money(money_str.get()))
    update_btn.grid(row=1,column=5)
    show_money_str = tk.StringVar()
    show_money_str.set('Now you have '+str(my_records._money)+' dollars')
    money_label = tk.Label(f,textvariable=show_money_str)
    money_label.grid(row=2,column=1)
    #find record
    find_label = tk.Label(f,text='Find category: ')
    find_label.grid(row=2,column=3)
    find_str = tk.StringVar()
    find_entry = tk.Entry(f,textvariable=find_str)
    find_entry.grid(row=2,column=4)
    find_btn = tk.Button(f,text='Find',command=lambda:find_record(find_str.get()))
    find_btn.grid(row=2,column=5)
    #delete record
    delete_btn = tk.Button(f,text='Delete selected record',command= lambda: delete_selected())
    delete_btn.grid(row=3,column=2)
    #show all records back
    show_records_back_btn = tk.Button(f,text='Show all records back',command= lambda:show_records_back())
    show_records_back_btn.grid(row=4,column=2)
    tk.mainloop()
    my_records.save()
    
    #print(my_records.items)
    """while(True):
        command = input('What do you want to do (add / view / delete / view categories / find / exit)?')
        if command == 'add':
            my_records.add()
        elif command == 'view':
            my_records.view()
        elif command == 'delete':
            my_records.delete()
        elif command == 'view categories':
            my_categories.view_categories()
        elif command == 'find':
            my_records.find()
        elif command == 'exit':
            my_records.save()
            break
        else:
            sys.stderr.write('Invalid command. Try again.\n')"""
    