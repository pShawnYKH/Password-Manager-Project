import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os
import sqlite3

__pass_code="udumbass"
__PASS_CODE=__pass_code.lower()
subpage_form_access=False  #debug
selected_subpage=None
FONT="Segoe UI Variable Small Semilig"


def check_password(entry, app):
    if entry.get().strip().lower()==__PASS_CODE or subpage_form_access:
        messagebox.showinfo("Success", "Access granted!")
        app.destroy()
        main_form()
    else:
        messagebox.showerror("Error", "Wrong password, try again.")

def login_form():
    log_app=tk.Tk()
    log_app.title("Passwords Manager Login")
    log_app.resizable(False, False)

    try:
        icon_path=resolve_path("locked_icon.ico")
        img_path=resolve_path("pass_icon.png")
        
        log_app.iconbitmap(icon_path)
        
        img=Image.open(img_path)
        photo_icon1=ImageTk.PhotoImage(img.resize((48, 48)))
        log_app.photo_icon1=photo_icon1

        pass_label=ttk.Label(log_app, 
                                text="Enter Password", 
                                font=(FONT, 16),
                                image=photo_icon1, 
                                compound="left")
    except Exception as e:
        print(f"Error loading images: {e}")
        pass_label=ttk.Label(log_app, text="Enter Password", font=(FONT, 16))

    pass_label.pack(pady=10)

    pass_entry=ttk.Entry(log_app, 
                           show="*", 
                           font=(FONT, 13), 
                           width=30)
    pass_entry.pack(padx=20)
    pass_entry.focus()

    login_button=tk.Button(log_app, 
                           text="Login", 
                           font=(FONT, 10), 
                           width=15, 
                           fg="#ffffff",
                           bg="#0078d4", 
                           bd=2,
                           command=lambda: check_password(pass_entry, log_app))
    login_button.pack(padx=20, pady=20, anchor='se')

    pass_entry.bind("<Return>", lambda e: check_password(pass_entry, log_app))
    
    center_window(log_app, 405, 167)
    log_app.mainloop()


def main_form():
    global selected_subpage
    selected_subpage="Home"
    main_app=tk.Tk()
    main_app.title("Password Manager")

    try:
        icon_path=resolve_path("unlocked_icon.ico")
        main_app.iconbitmap(icon_path)
    except Exception:
        pass

    main_app.resizable(False, False)
    
    manager=tk.Frame(main_app)
    manager.pack(fill="both", expand=True)
    manager.grid_rowconfigure(0, weight=1)
    manager.grid_rowconfigure(1, weight=0)
    manager.grid_columnconfigure(0, weight=0)
    manager.grid_columnconfigure(1, weight=1)
    
    nav_container=tk.Frame(manager, bg="#f2f3f5", width=260)
    nav_container.grid(row=0, column=0, sticky="ns")
    nav_container.pack_propagate(False)
    
    tk.Label(nav_container, 
             text="Subpages", 
             font=(FONT, 12, "bold"), 
             bg="#f2f3f5").pack(anchor="w", padx=15, pady=(10, 5))
    
    canvas, scroll_frame=setup_scrollable_frame(nav_container)
    
    content=tk.Frame(manager, bg="white")
    content.grid(row=0, column=1, sticky="nsew")
    
    create_subpage_labels(scroll_frame, "Home", content, canvas)

    connect=get_db()
    subpages=connect.execute("SELECT name FROM subpages").fetchall()
    connect.close()

    for row in subpages:
        create_subpage_labels(scroll_frame, row['name'], content, canvas)
        
    show_subpage(content, "Home")
    
    footer=tk.Frame(manager, bg="#f9f9f9")
    footer.grid(row=1, column=0, columnspan=2, sticky="ew")
    tk.Frame(footer, height=1, bg="#e0e0e0").pack(fill="x")
    
    btn_container=tk.Frame(footer, bg="#f9f9f9")
    btn_container.pack(fill="x", pady=8)
    
    tk.Button(btn_container, 
              text="+ Add Subpage", 
              font=(FONT, 9), 
              relief="raised", 
              bg="#e0e0e0", 
              bd=2,
              command=lambda: add_subpage(scroll_frame, canvas, content)).pack(side="left", padx=6)
    
    tk.Button(btn_container, 
              text="      Rename      ", 
              font=(FONT, 9), 
              relief="raised", 
              bg="#e0e0e0", 
              bd=2,
              command=lambda: rename_subpage(scroll_frame, content, canvas)).pack(side="left")
    
    tk.Button(btn_container, 
              text="        Delete        ", 
              font=(FONT, 9), 
              relief="raised", 
              fg="#ffffff", 
              bg="#d32f2f", 
              bd=2,
              command=lambda: delete_subpage(scroll_frame, content, canvas)).pack(side="left", padx=6)
    
    def check_add_account():
        print(f"DEBUG: Attempting Add Account. Current Page: {selected_subpage}")

        if selected_subpage=="Home":
            messagebox.showinfo("Invalid Selection", "Cannot add an account inside 'Home.'")
        else:
            add_account_dialog(content, selected_subpage)

    tk.Button(btn_container, 
              text="+ Add Account", 
              font=(FONT, 9), 
              bg="#0078d4", 
              fg="white", 
              relief="raised", 
              bd=2, 
              padx=1,
              command=check_add_account).pack(side="right", padx=6)
    
    main_app.protocol("WM_DELETE_WINDOW", lambda: verify_close(main_app))
    
    center_window(main_app, 800, 911)
    main_app.mainloop()

def verify_close(main_app):
    if messagebox.askyesno("Quit?", "Are you sure you want to quit?"):
        main_app.destroy()

def show_home_page(content_frame):
    frame=tk.Frame(content_frame, bg="white")
    frame.pack(fill="both", expand=True, padx=40, pady=30)
    
    tk.Label(frame, 
             text="Password Manager", 
             font=(FONT, 20, "bold"), 
             bg="white").pack(pady=(0, 0))
    
    text_widget=tk.Text(frame, font=(FONT, 11), bg="white", relief="flat", wrap="word", height=20)

    text_widget.insert("end", home_text, "bold")
    text_widget.insert("end", home_text2)
    text_widget.insert("end", home_text3, "bold")
    text_widget.insert("end", home_text4)
    text_widget.insert("end", home_text5, "bold")
    text_widget.insert("end", home_text6)
    text_widget.insert("end", home_text7, "bold")
    text_widget.insert("end", home_text8)
    text_widget.insert("end", home_text9, "bold")
    text_widget.insert("end", home_text10)
    text_widget.insert("end", home_text11, "bold")
    text_widget.insert("end", home_text12)

    text_widget.config(state="disabled")
    text_widget.tag_configure("bold", font=(FONT, 12, "bold"))
    text_widget.pack(fill="both", expand=True)

home_text="""
Welcome to Password Manager!
"""

home_text2="""
This is a simple desktop app made with Python and Tkinter to manage your accounts and passwords. You can create subpages to organize accounts however you want, add new usernames and passwords, rename or delete subpages, and easily see all your accounts. The sidebar lets you scroll through your subpages, and the main area shows account details. It has a login for access and footer buttons for quick subpage actions. Clean, simple, and easy to use.

"""

home_text3="""
Getting Started:"""

home_text4="""
• Click '+ Add Subpage' to create categories for your passwords
• Add accounts within each subpage to organize your credentials
• Use the 'Show' button to hide/unhide your passwords
"""

home_text5="""
Features:"""

home_text6="""
• Organize passwords by category (Work, Games, Socials, etc.)
• Secure password storage with database integration
• Easy-to-use interface for managing multiple accounts
"""

home_text7="""
Tips:"""

home_text8="""
• Use strong, unique passwords for each account
• Create subpages to organize passwords by purpose
• Click 'Save' to persist your data (database not yet implemented)
"""

home_text9="""

Credits:
"""

home_text10="""This application was made by:
"""

home_text11="""
                      Shawn Yash Kyler H. Pesquisa
"""

home_text12="""
As a final project in Advanced Computer Programming (ACP) in order to continue to develop his programming skills and eventually be of use in the near future."""


def show_subpage(content_frame, name):
    global selected_subpage
    selected_subpage=name
    
    for w in content_frame.winfo_children():
        w.destroy()
    
    if name=="Home":
        show_home_page(content_frame)
        return
    
    header=tk.Frame(content_frame, 
                      bg="white")
    header.pack(fill="x", padx=20, pady=(15, 5))
    
    tk.Label(header, 
             text=f"{name} Accounts", 
             font=(FONT, 16, "bold"), 
             bg="white").pack(side="left")
    
    canvas, scrollable_frame=setup_scrollable_frame(content_frame, bg="white")

    connect=get_db()
    cursor=connect.cursor()
    cursor.execute("SELECT * FROM accounts WHERE subpage_name = ?", (name,))
    accounts=[dict(row) for row in cursor.fetchall()]
    connect.close()
    
    if not accounts:
        tk.Label(scrollable_frame, 
                 text="No accounts yet. Click '+ Add Account' to create one.", 
                 fg="#999999", 
                 bg="white", 
                 font=(FONT, 10)).pack(pady=40)
    else:
        for acc in accounts:
            create_account_frame(scrollable_frame, acc, name, content_frame)

def create_subpage_labels(parent, name, content_frame, canvas):
    is_selected=name==selected_subpage
    btn_frame=tk.Frame(parent, 
                           bg="#f2f3f5")
    btn_frame.pack(fill="x", pady=1)
    
    tk.Frame(btn_frame, 
             bg="#0078d4" if is_selected else "#f2f3f5", 
             width=4).pack(side="left", fill="y")
    btn=tk.Label(btn_frame, 
                    text=name, 
                    anchor="w", 
                    bg="#e8e9eb" if is_selected else "#f2f3f5", 
                    padx=12, 
                    pady=10, 
                    font=(FONT, 10))
    btn.pack(side="left", fill="both", expand=True)
    
    btn.bind("<Button-1>", lambda e: (show_subpage(content_frame, name), refresh_subpage_list(parent, content_frame, canvas)))
    if not is_selected:
        btn.bind("<Enter>", lambda e: btn.config(bg="#e1e2e5"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#f2f3f5"))

def refresh_subpage_list(parent, content_frame, canvas):
    for widget in parent.winfo_children():
        widget.destroy()

    create_subpage_labels(parent, "Home", content_frame, canvas)

    connect=get_db()
    subpages=connect.execute("SELECT name FROM subpages").fetchall()
    connect.close()
    
    for row in subpages:
        create_subpage_labels(parent, row['name'], content_frame, canvas)

def add_subpage(scroll_frame, canvas, content_frame):
    dialog=create_dialog("Add Subpage", 360, 140)

    tk.Label(dialog, text="Subpage Name:", font=(FONT, 11)).pack(anchor="w", padx=20, pady=(20, 5))
    entry=tk.Entry(dialog, font=(FONT, 10), width=35)
    entry.pack(padx=20, pady=(0, 10))

    def save():
        name=entry.get().strip()
        if not name or name=="Home":
            messagebox.showwarning("Invalid Input", "Name invalid.")
            return

        try:
            connect=get_db()
            connect.execute("INSERT INTO subpages (name) VALUES (?)", (name,))
            connect.commit()
            connect.close()
            
            dialog.destroy()
            refresh_subpage_list(scroll_frame, content_frame, canvas)
            show_subpage(content_frame, name)
        except sqlite3.IntegrityError:
            messagebox.showwarning("Error", "Name already exists.")
            connect.close()

    create_dialog_buttons(dialog, save)
    entry.focus()

def delete_subpage(scroll_frame, content_frame, canvas):
    global selected_subpage
    if not selected_subpage or selected_subpage=="Home":
        messagebox.showinfo("Denied", "Cannot delete Home.")
        return

    dialog=create_dialog("Delete Subpage", 360, 120)

    tk.Label(dialog,
             text=f"Delete '{selected_subpage}' and all its accounts?",
             font=(FONT, 11),
             wraplength=340,
             justify="left").pack(anchor="center", padx=20, pady=(20, 10))

    def save():
        global selected_subpage

        connect=get_db()
        connect.execute("DELETE FROM subpages WHERE name = ?", (selected_subpage,))
        connect.commit()
        connect.close()

        selected_subpage="Home"
        dialog.destroy()
        refresh_subpage_list(scroll_frame, content_frame, canvas)
        show_subpage(content_frame, "Home")

    create_dialog_buttons(dialog, save, save_text="Delete", save_color="#d32f2f", save_fg="white")

def rename_subpage(scroll_frame, content_frame, canvas):
    global selected_subpage
    if not selected_subpage or selected_subpage=="Home":
        messagebox.showinfo("Denied", "Cannot rename Home.")
        return

    dialog=create_dialog("Rename Subpage", 360, 140)

    tk.Label(dialog, text=f"Rename '{selected_subpage}' to:", font=(FONT, 10))\
        .pack(anchor="w", padx=20, pady=(20, 5))

    entry=tk.Entry(dialog, font=(FONT, 11), width=35)
    entry.pack(padx=20, pady=(0, 10))
    entry.insert(0, selected_subpage)
    entry.focus()

    def save():
        global selected_subpage
        new_name=entry.get().strip()
        if not new_name or new_name=="Home":
            messagebox.showwarning("Invalid", "Name invalid.")
            return
        
        try:
            connect=get_db()
            connect.execute("UPDATE subpages SET name = ? WHERE name = ?", (new_name, selected_subpage))
            connect.commit()
            connect.close()
            
            selected_subpage=new_name
            dialog.destroy()
            refresh_subpage_list(scroll_frame, content_frame, canvas)
            show_subpage(content_frame, new_name)
        except sqlite3.IntegrityError:
            messagebox.showwarning("Error", "Name already exists.")
            connect.close()

    create_dialog_buttons(dialog, save)


def create_account_frame(parent, account, subpage_name, content_frame):
    acc_frame=tk.Frame(parent, bg="white", relief="flat", bd=0)
    acc_frame.pack(fill="x", padx=20, pady=15)
    
    tk.Label(acc_frame, text=f"{account.get('name', 'Unnamed')}", 
             font=(FONT, 11, "bold"), bg="white").pack(anchor="w")
    tk.Frame(acc_frame, height=1, bg="#e0e0e0").pack(fill="x", pady=(5, 12))

    for field_name, field_key in [("Username", "username"), ("Email", "email"), ("Password", "password")]:
        tk.Label(acc_frame, text=field_name, font=(FONT, 9), fg="#666666", bg="white").pack(fill="x", pady=(0, 2))
        
        if field_key=="password":
            pwd_frame=tk.Frame(acc_frame, bg="white")
            pwd_frame.pack(fill="x", pady=(0, 12))
            pwd_entry=tk.Entry(pwd_frame, font=(FONT, 10), show="*", relief="solid", bd=1)
            pwd_entry.insert(0, account.get(field_key, ''))
            pwd_entry.config(state="readonly")
            pwd_entry.pack(side="left", fill="x", expand=True, ipady=6)
            
            show_btn=tk.Button(pwd_frame, text="Show", font=(FONT, 11), relief="solid", bd=1, bg="#e0e0e0")
            show_btn.config(command=lambda e=pwd_entry, b=show_btn: toggle_password(e, b))
            show_btn.pack(side="right", padx=(5, 0))
        else:
            entry=tk.Entry(acc_frame, font=(FONT, 10), relief="solid", bd=1)
            entry.insert(0, account.get(field_key, ''))
            entry.config(state="readonly")
            entry.pack(fill="x", ipady=6, pady=(0, 12))
    
    btn_frame=tk.Frame(acc_frame, bg="white")
    btn_frame.pack(fill="x", pady=(8, 0))
    tk.Button(btn_frame, text="        Change        ", fg="#000000", bg="#e0e0e0", font=(FONT, 9), relief="raised", bd=2,
              command=lambda: change_account(account, subpage_name, content_frame)).pack(side="left")
    tk.Button(btn_frame, text="          Delete          ", fg="#ffffff", bg="#d32f2f", font=(FONT, 9), relief="raised", bd=2,
              command=lambda: delete_account(account, subpage_name, content_frame)).pack(side="right")

def toggle_password(entry, btn):
    entry.config(show='' if entry.cget('show')=='*' else '*')

def delete_account(account, subpage_name, content_frame):
    if messagebox.askyesno("Delete Account?", f"Delete '{account.get('name', 'this account')}'?"):

        connect=get_db()
        connect.execute("DELETE FROM accounts WHERE id = ?", (account['id'],))
        connect.commit()
        connect.close()

        show_subpage(content_frame, subpage_name)

def change_account(account, subpage_name, content_frame):
    dialog=create_dialog("Change Account", 400, 300)
    fields={}
    
    for label, key in [("Account Name", "name"), ("Username", "username"), ("Email", "email"), ("Password", "password")]:
        tk.Label(dialog, text=f"{label}:", font=(FONT, 10)).pack(anchor="w", padx=20, pady=(10 if label=="Account Name" else 0, 5))
        fields[key]=tk.Entry(dialog, font=(FONT, 10), width=40)
        fields[key].insert(0, account.get(key, ''))
        fields[key].pack(padx=20, pady=(0, 10))
    
    def save():
        new_data={k: v.get().strip() for k, v in fields.items()}

        connect=get_db()
        connect.execute("""
            UPDATE accounts 
            SET name=?, username=?, email=?, password=?
            WHERE id=?
        """, (new_data['name'], new_data['username'], new_data['email'], new_data['password'], account['id']))
        connect.commit()
        connect.close()
        
        dialog.destroy()
        show_subpage(content_frame, subpage_name)
    
    create_dialog_buttons(dialog, save)

def add_account_dialog(content_frame, subpage_name):
    dialog=create_dialog("Add New Account", 400, 300)
    fields={}
    
    for label, key in [("Account Name", "name"), ("Username", "username"), ("Email", "email"), ("Password", "password")]:
        tk.Label(dialog, text=f"{label}:", font=(FONT, 10)).pack(anchor="w", padx=20, pady=(10 if label=="Account Name" else 0, 5))
        fields[key]=tk.Entry(dialog, font=(FONT, 10), width=40)
        fields[key].pack(padx=20, pady=(0, 10))
    
    def save():
        data={k: v.get().strip() for k, v in fields.items()}
        if not data['name'] or not data['username'] or not data['password']:
            messagebox.showwarning("Missing Info", "Please fill in Account Name, Username, and Password.")
            return
        
        connect=get_db()
        connect.execute("""
            INSERT INTO accounts (subpage_name, name, username, email, password)
            VALUES (?, ?, ?, ?, ?)
        """, (subpage_name, data['name'], data['username'], data['email'], data['password']))
        connect.commit()
        connect.close()
        
        dialog.destroy()
        show_subpage(content_frame, subpage_name)
    
    create_dialog_buttons(dialog, save)
    fields['name'].focus()


def center_window(window, width, height):
    window.update_idletasks()
    x=(window.winfo_screenwidth() // 2) - (width // 2)
    y=(window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def setup_scrollable_frame(parent, bg="#f2f3f5"):
    canvas=tk.Canvas(parent, bg=bg, highlightthickness=0)
    vsb=tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scroll_frame=tk.Frame(canvas, bg=bg)
    
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    window_id=canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))
    
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", 
                lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    
    return canvas, scroll_frame

def create_dialog(title, width, height):
    dialog_app=tk.Toplevel()
    dialog_app.title(title)
    dialog_app.geometry(f"{width}x{height}")
    dialog_app.resizable(False, False)
    dialog_app.grab_set()
    center_window(dialog_app, width, height)
    return dialog_app

def create_dialog_buttons(dialog, save_cmd, save_text="Save", save_color="#0078d4", save_fg="white"):
    btn_frame=tk.Frame(dialog)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, 
              text=save_text, 
              bg=save_color, 
              fg=save_fg, 
              font=(FONT, 10), 
              width=10, 
              relief="raised", 
              bd=2, 
              command=save_cmd).pack(side="left", padx=7, anchor="se")
    tk.Button(btn_frame, 
              text="Cancel", 
              font=(FONT, 10), 
              width=10, 
              bg="#e0e0e0",
              relief="raised", 
              bd=2, 
              command=dialog.destroy).pack(side="left", padx=7, anchor="se")
    
def resolve_path(filename):
    base_path=os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)


def get_db():
    connect=sqlite3.connect(resolve_path("passwords.db"))
    connect.execute("PRAGMA foreign_keys = 1")
    connect.row_factory=sqlite3.Row 
    return connect

def init_db():
    connect=get_db()
    cursor=connect.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subpages (
            name TEXT PRIMARY KEY
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subpage_name TEXT,
            name TEXT,
            username TEXT,
            email TEXT,
            password TEXT,
            FOREIGN KEY(subpage_name) REFERENCES subpages(name) 
            ON DELETE CASCADE ON UPDATE CASCADE
        )
    """)
    connect.commit()
    connect.close()
    

if __name__=="__main__":
    init_db()
    login_form()