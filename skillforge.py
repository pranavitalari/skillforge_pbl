from tkinter import *
from tkinter import ttk, messagebox
import json
import os

# -------------------- WINDOW --------------------

root = Tk()
root.title("SkillForge - Personal Skill Growth Tracker")
root.geometry("1400x850")
root.resizable(True, True)
root.configure(bg="#F4F7FB")

# -------------------- DATA FILE --------------------

FILE_NAME = "skills.json"
skills = []

def load_data():
    global skills

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                skills = json.load(file)
        except:
            skills = []
    else:
        skills = []

def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(skills, file, indent=4)

# -------------------- STYLE --------------------

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold"),
    background="#512DA8",
    foreground="white"
)

style.configure(
    "Treeview",
    font=("Arial", 10),
    rowheight=30
)

style.configure(
    "TNotebook.Tab",
    font=("Arial", 11, "bold"),
    padding=10
)

# -------------------- TITLE --------------------

title = Label(
    root,
    text="🎯 SkillForge - Personal Skill Growth Tracker",
    font=("Arial", 24, "bold"),
    bg="#512DA8",
    fg="white",
    pady=18
)

title.pack(fill=X)

# -------------------- INPUT FORM --------------------

form = Frame(root, bg="#F4F7FB")
form.pack(pady=15)

Label(
    form,
    text="Skill ID",
    font=("Arial", 12),
    bg="#F4F7FB"
).grid(row=0, column=0, padx=10, pady=8)

id_entry = Entry(form, font=("Arial", 12), width=20)
id_entry.grid(row=0, column=1)

Label(
    form,
    text="Skill Name",
    font=("Arial", 12),
    bg="#F4F7FB"
).grid(row=0, column=2, padx=10)

name_entry = Entry(form, font=("Arial", 12), width=20)
name_entry.grid(row=0, column=3)

Label(
    form,
    text="Category",
    font=("Arial", 12),
    bg="#F4F7FB"
).grid(row=1, column=0, padx=10, pady=8)

categories = [
    "Programming",
    "Communication",
    "Technical",
    "Personal Development",
    "Other"
]

category_entry = ttk.Combobox(
    form,
    font=("Arial", 12),
    width=18,
    values=categories,
    state="readonly"
)

category_entry.grid(row=1, column=1)

Label(
    form,
    text="Start Date",
    font=("Arial", 12),
    bg="#F4F7FB"
).grid(row=1, column=2, padx=10)

start_entry = Entry(form, font=("Arial", 12), width=20)
start_entry.grid(row=1, column=3)

Label(
    form,
    text="Target Date",
    font=("Arial", 12),
    bg="#F4F7FB"
).grid(row=2, column=0, padx=10, pady=8)

target_entry = Entry(form, font=("Arial", 12), width=20)
target_entry.grid(row=2, column=1)

Label(
    form,
    text="Progress (%)",
    font=("Arial", 12),
    bg="#F4F7FB"
).grid(row=2, column=2, padx=10)

progress_entry = Entry(form, font=("Arial", 12), width=20)
progress_entry.grid(row=2, column=3)

Label(
    form,
    text="Status",
    font=("Arial", 12),
    bg="#F4F7FB"
).grid(row=3, column=0, padx=10, pady=8)

status_entry = ttk.Combobox(
    form,
    font=("Arial", 12),
    width=18,
    values=["Not Started", "In Progress", "Completed"],
    state="readonly"
)

status_entry.grid(row=3, column=1)

Label(
    form,
    text="Notes",
    font=("Arial", 12),
    bg="#F4F7FB"
).grid(row=3, column=2, padx=10)

notes_entry = Entry(form, font=("Arial", 12), width=20)
notes_entry.grid(row=3, column=3)

# -------------------- CATEGORY TABLES --------------------

notebook = ttk.Notebook(root)

tables = {}

columns = (
    "ID",
    "Skill Name",
    "Category",
    "Start Date",
    "Target Date",
    "Progress",
    "Status",
    "Notes"
)

for cat in categories:

    frame = Frame(notebook, bg="#F4F7FB")

    notebook.add(frame, text=cat)

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    for col in columns:

        tree.heading(col, text=col)

        tree.column(col, width=150, anchor=CENTER)

    tree.column("Skill Name", width=180)
    tree.column("Notes", width=220)

    vsb = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=tree.yview
    )

    hsb = ttk.Scrollbar(
        frame,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=vsb.set,
        xscrollcommand=hsb.set
    )

    tree.grid(row=0, column=0, sticky="nsew")

    vsb.grid(row=0, column=1, sticky="ns")

    hsb.grid(row=1, column=0, sticky="ew")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    tables[cat] = tree

# -------------------- FUNCTIONS --------------------

def clear_entries():

    id_entry.delete(0, END)
    name_entry.delete(0, END)
    category_entry.set("")
    start_entry.delete(0, END)
    target_entry.delete(0, END)
    progress_entry.delete(0, END)
    status_entry.set("")
    notes_entry.delete(0, END)


def refresh_tables():

    for cat in categories:

        tables[cat].delete(*tables[cat].get_children())

    for item in skills:

        cat = item["category"]

        if cat in tables:

            tables[cat].insert(
                "",
                END,
                values=(
                    item["id"],
                    item["name"],
                    item["category"],
                    item["start"],
                    item["target"],
                    str(item["progress"]) + "%",
                    item["status"],
                    item["notes"]
                )
            )


# -------------------- DASHBOARD --------------------

def update_dashboard():

    total = len(skills)

    completed = 0
    in_progress = 0
    average = 0

    if total > 0:

        progress_total = 0

        for item in skills:

            progress_total += int(item["progress"])

            if item["status"] == "Completed":
                completed += 1

            elif item["status"] == "In Progress":
                in_progress += 1

        average = progress_total / total

    total_label.config(
        text="Total Skills : {}".format(total)
    )

    completed_label.config(
        text="Completed : {}".format(completed)
    )

    progress_label.config(
        text="In Progress : {}".format(in_progress)
    )

    average_label.config(
        text="Average Progress : {:.1f}%".format(average)
    )


# -------------------- GET FORM DATA --------------------

def get_form_data():

    skill_id = id_entry.get().strip()
    name = name_entry.get().strip()
    category = category_entry.get()
    start = start_entry.get().strip()
    target = target_entry.get().strip()
    progress = progress_entry.get().strip()
    status = status_entry.get()
    notes = notes_entry.get().strip()

    if not skill_id or not name or not category:
        messagebox.showerror(
            "Error",
            "Skill ID, Skill Name and Category are required."
        )
        return None

    try:
        progress = int(progress)

        if progress < 0 or progress > 100:
            messagebox.showerror(
                "Error",
                "Progress must be between 0 and 100."
            )
            return None

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter a valid progress percentage."
        )
        return None

    if not status:
        messagebox.showerror(
            "Error",
            "Please select skill status."
        )
        return None

    return {
        "id": skill_id,
        "name": name,
        "category": category,
        "start": start,
        "target": target,
        "progress": progress,
        "status": status,
        "notes": notes
    }


# -------------------- ADD SKILL --------------------

def add_skill():

    skill = get_form_data()

    if skill is None:
        return

    for item in skills:

        if item["id"] == skill["id"]:
            messagebox.showerror(
                "Error",
                "Skill ID already exists."
            )
            return

    skills.append(skill)

    save_data()
    refresh_tables()
    update_dashboard()
    clear_entries()

    messagebox.showinfo(
        "Success",
        "Skill Added Successfully."
    )


# -------------------- ACTIVE CATEGORY --------------------

def get_active_category():

    return notebook.tab(
        notebook.select(),
        "text"
    )


# -------------------- EDIT SKILL --------------------

def edit_skill():

    cat = get_active_category()

    selected = tables[cat].focus()

    if selected == "":
        messagebox.showerror(
            "Error",
            "Select a skill from the table."
        )
        return

    values = tables[cat].item(
        selected,
        "values"
    )

    old_id = values[0]

    skill = get_form_data()

    if skill is None:
        return

    for item in skills:

        if item["id"] == skill["id"] and item["id"] != old_id:

            messagebox.showerror(
                "Error",
                "Skill ID already exists."
            )
            return

    for i, item in enumerate(skills):

        if item["id"] == old_id and item["category"] == cat:

            skills[i] = skill
            break

    save_data()
    refresh_tables()
    update_dashboard()
    clear_entries()

    messagebox.showinfo(
        "Success",
        "Skill Updated Successfully."
    )


# -------------------- DELETE SKILL --------------------

def delete_skill():

    cat = get_active_category()

    selected = tables[cat].focus()

    if selected == "":
        messagebox.showerror(
            "Error",
            "Select a skill to delete."
        )
        return

    values = tables[cat].item(
        selected,
        "values"
    )

    skill_id = values[0]

    if messagebox.askyesno(
        "Delete",
        "Do you want to delete this skill?"
    ):

        for i, item in enumerate(skills):

            if item["id"] == skill_id and item["category"] == cat:

                skills.pop(i)
                break

        save_data()
        refresh_tables()
        update_dashboard()
        clear_entries()

        messagebox.showinfo(
            "Deleted",
            "Skill Deleted Successfully."
        )


# -------------------- CLEAR ALL SKILLS --------------------

def clear_all():

    if messagebox.askyesno(
        "Clear All",
        "Do you want to delete ALL skills?"
    ):

        skills.clear()

        save_data()
        refresh_tables()
        update_dashboard()
        clear_entries()

        messagebox.showinfo(
            "Cleared",
            "All Skills Deleted Successfully."
        )


# -------------------- REFRESH --------------------

def refresh_all():

    clear_entries()
    refresh_tables()
    update_dashboard()


# -------------------- SELECT TABLE ITEM --------------------

def on_item_select(event):

    cat = get_active_category()

    selected = tables[cat].focus()

    if selected:

        values = tables[cat].item(
            selected,
            "values"
        )

        id_entry.delete(0, END)
        id_entry.insert(0, values[0])

        name_entry.delete(0, END)
        name_entry.insert(0, values[1])

        category_entry.set(values[2])

        start_entry.delete(0, END)
        start_entry.insert(0, values[3])

        target_entry.delete(0, END)
        target_entry.insert(0, values[4])

        progress_entry.delete(0, END)
        progress_entry.insert(0, values[5].replace("%", ""))

        status_entry.set(values[6])

        notes_entry.delete(0, END)
        notes_entry.insert(0, values[7])


for cat in categories:

    tables[cat].bind(
        "<<TreeviewSelect>>",
        on_item_select
    )


# -------------------- BUTTONS --------------------

button_frame = Frame(
    root,
    bg="#F4F7FB"
)

ttk.Button(
    button_frame,
    text="➕ Add Skill",
    command=add_skill
).grid(row=0, column=0, padx=8)

ttk.Button(
    button_frame,
    text="✏️ Edit Skill",
    command=edit_skill
).grid(row=0, column=1, padx=8)

ttk.Button(
    button_frame,
    text="❌ Delete Skill",
    command=delete_skill
).grid(row=0, column=2, padx=8)

ttk.Button(
    button_frame,
    text="🧹 Clear Fields",
    command=clear_entries
).grid(row=0, column=3, padx=8)

ttk.Button(
    button_frame,
    text="🔄 Refresh",
    command=refresh_all
).grid(row=0, column=4, padx=8)

ttk.Button(
    button_frame,
    text="🗑️ Clear All Skills",
    command=clear_all
).grid(row=0, column=5, padx=8)


# -------------------- DASHBOARD --------------------

dashboard = Frame(
    root,
    bg="#EDE7F6",
    pady=15
)

total_label = Label(
    dashboard,
    text="Total Skills : 0",
    font=("Arial", 13, "bold"),
    bg="#EDE7F6",
    fg="#4527A0"
)

total_label.pack(side=LEFT, padx=25)

completed_label = Label(
    dashboard,
    text="Completed : 0",
    font=("Arial", 13, "bold"),
    bg="#EDE7F6",
    fg="#2E7D32"
)

completed_label.pack(side=LEFT, padx=25)

progress_label = Label(
    dashboard,
    text="In Progress : 0",
    font=("Arial", 13, "bold"),
    bg="#EDE7F6",
    fg="#EF6C00"
)

progress_label.pack(side=LEFT, padx=25)

average_label = Label(
    dashboard,
    text="Average Progress : 0%",
    font=("Arial", 13, "bold"),
    bg="#EDE7F6",
    fg="#1565C0"
)

average_label.pack(side=LEFT, padx=25)


# -------------------- DISPLAY BUTTONS --------------------

button_frame.pack(pady=10)

# -------------------- DISPLAY DASHBOARD --------------------

dashboard.pack(fill=X)

# -------------------- DISPLAY TABLE --------------------

notebook.pack(
    pady=10,
    fill=BOTH,
    expand=True
)


# -------------------- INITIALIZATION --------------------

load_data()
refresh_tables()
update_dashboard()


# -------------------- MAIN LOOP --------------------

root.mainloop()