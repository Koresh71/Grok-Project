import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import json, os, sys, hashlib, uuid, webbrowser, base64, glob

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except: pass

# --- ТЕХНИЧЕСКИЕ ДАННЫЕ ---
ENCODED_SALT = "R1JPSy1QUk8tS09STklMT1YtVjE="
SECRET_SALT = base64.b64decode(ENCODED_SALT).decode('utf-8')

BG_MAIN, BG_PANEL = "#1c1c1c", "#262626" 
ACCENT, ACCENT_2 = "#10b981", "#059669" 
TEXT_MAIN, TEXT_DESC, TEXT_MUTED = "#ffffff", "#d1fae5", "#94a3b8"
SUCCESS, DANGER = "#84cc16", "#ef4444"

def get_base_path():
    if getattr(sys, 'frozen', False): return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# --- ПОЛНЫЕ ТЕКСТЫ ИНФОРМАЦИЯ (БЕЗ СОКРАЩЕНИЙ) ---
INFO_RU = """Как генерировать вирусные ролики в Grok Imagine
Работа с Grok строится на правиле «Бей сразу».
У тебя есть всего несколько секунд, поэтому медленные раскадровки здесь не работают. Следуй этим правилам, чтобы получить максимальный результат:

Шаг 1. Формула идеального старта («Start with...»)
Grok лучше всего работает, когда четко понимает, как выглядит первый кадр. Наши промты всегда начинаются с описания стартовой композиции (например: Start with an extreme macro close-up of a...). Нейросеть сначала «рисует» эту картинку у себя в «голове», а затем приводит ее в движение. Не меняй это начало!

Шаг 2. Правило 6 секунд (The 6-Second Rule)
Помни, что Grok официально генерирует очень короткие видео. Всё действие в промте должно умещаться в этот лимит.

Совет режиссера: Пиши агрессивные глаголы. Не «машина едет», а «машина яростно срывается с места, выбрасывая грязь в линзу» (aggressively spins out, kicking up a massive cloud of mud).

Шаг 3. Задавай движение камеры
В отличие от других сетей, Grok любит динамичную, иногда грязную съемку. Вставляй в промты фразы вроде:
Aggressive camera shake (Агрессивная тряска камеры — для взрывов).
Fast-tracking shot (Быстрое следование).
Subjective POV (Вид от первого лица).

Шаг 4. Не бойся абсурда (Embrace the Weird)
Grok создавался как нейросеть без жестких творческих ограничений (в разумных пределах). Если ты хочешь сгенерировать 50-метрового хомяка, крутящего колесо обозрения в центре Нью-Йорка — просто попроси его об этом. Чем безумнее сочетание несочетаемого, тем круче результат.

Шаг 5. Как использовать нашу базу
Скопируй нужный промт на английском (от слова Start и до конца). Вставь в строку генерации Grok. Если нужно адаптировать идею, просто замени существительные. Например, в промте про «кота-бухгалтера» поменяй grumpy, fat tabby cat на cute golden retriever — и получишь собаку-бухгалтера, сохранив всю остальную идеальную физику сцены."""

INFO_EN = """How to Generate Viral Videos in Grok Imagine
Working with Grok is based on the "Hit Hard" rule.
You only have a few seconds, so slow storyboards don't work here. Follow these rules to get maximum results:

Step 1. The Perfect Start Formula ("Start with...")
Grok works best when it clearly understands what the first frame looks like. Our prompts always begin with a description of the starting composition (e.g., Start with an extreme macro close-up of a...). The AI first "paints" this image in its "mind" and then sets it in motion. Do not change this opening!

Step 2. The 6-Second Rule. Remember that Grok generates very short videos. All action in the prompt must fit within this limit.

Director's Tip: Use aggressive verbs. Instead of "a car is driving," use "a car aggressively spins out, kicking up a massive cloud of mud into the lens" (aggressively spins out, kicking up a massive cloud of mud).

Step 3. Set the Camera Movement. Unlike other networks, Grok loves dynamic, sometimes gritty cinematography. Insert phrases into your prompts like:
Aggressive camera shake (For explosions).
Fast-tracking shot (Fast tracking).
Subjective POV (First-person view).

Step 4. Embrace the Weird. Grok was created as an AI without rigid creative boundaries (within reasonable limits). If you want to generate a 50-meter hamster spinning a Ferris wheel in the center of New York — just ask for it. The crazier the combination of the mismatched, the better the result.

Step 5. How to Use Our Database
Copy the required prompt in English (from the word Start to the end). Paste it into the Grok generation line. If you need to adapt the idea, simply replace the nouns. For example, in the prompt about the "accountant cat," change grumpy, fat tabby cat to cute golden retriever — and you'll get an accountant dog while preserving all the other perfect physics of the scene."""

HELP_RU = """📝 Инструкция по использованию программы:
1. Поиск: Во вкладке 'База Промптов' выберите категорию в списке слева. Нажмите на название эффекта.
2. Копирование: Нажмите кнопку 'КОПИРОВАТЬ ПРОМПТ'. Текст скопируется в буфер обмена.
3. Управление: Во вкладке 'Управление базой' можно добавлять свои наработки (+).
4. Редактирование: Выберите свой промпт (user), измените поля и нажмите 'СОХРАНИТЬ'.
5. База: Программа видит все файлы *_grok_prompts.dat."""

HELP_EN = """📝 Program Usage Instructions:
1. Search: Select a category and effect from the list on the left. Click on the name to see description.
2. Copying: Click 'COPY PROMPT' to save text to clipboard.
3. Management: Add your own work in the 'Management' tab. Click '+' to create a category.
4. Editing: Only user prompts can be modified. Edit fields and click 'SAVE'.
5. Database: Automatically loads all files ending in _grok_prompts.dat."""

ABOUT_RU = "🧠 Grok Prompt Manager PRO\n\nВерсия: V 1.1\nЛицензия: АКТИВИРОВАНА ✅\nID: {hwid}\nРазработчик: IK Designs\n\nПрограмма предназначена для управления и быстрой генерации промптов для нейросети Grok Imagine. Все права защищены."
ABOUT_EN = "🧠 Grok Prompt Manager PRO\n\nVersion: V 1.1\nLicense: ACTIVATED ✅\nID: {hwid}\nDeveloper: IK Designs\n\nThe program is designed for managing and quickly generating prompts for the Grok Imagine AI. All rights reserved."

LANG_DATA = {
    "RU": {
        "title": "Grok Prompt Manager PRO", "tab_main": "💻 База Промптов", "tab_admin": "⚙ Управление базой",
        "tab_info": "📖 Информация", "tab_help": "📝 Инструкция", "nav": "🧭 НАВИГАЦИЯ", "all_cats": "Все категории",
        "copy_btn": "🚀 КОПИРОВАТЬ ПРОМПТ", "save_btn": "💾 СОХРАНИТЬ", "del_btn": "🗑 УДАЛИТЬ ПУНКТ",
        "add_new": "➕ ДОБАВИТЬ НОВЫЙ ПРОМТ", "cat_label": "1. КАТЕГОРИЯ:", "name_label": "2. НАЗВАНИЕ ЭФФЕКТА:",
        "desc_label": "3. ОПИСАНИЕ (RU):", "prompt_label": "4. ПРОМПТ (EN):", "lang_btn": "Language: EN", "zoom_btn": "🔍 МАСШТАБ",
        "about_btn": "ℹ О ПРОГРАММЕ", "auth_title": "АКТИВАЦИЯ ПРОГРАММЫ", "auth_hwid": "ID устройства:", "auth_copy_id": "📋 Копировать ID",
        "auth_paste": "📥 ВСТАВИТЬ", "auth_activate": "АКТИВИРОВАТЬ", "auth_back": "↩ СМЕНИТЬ ЯЗЫК", "auth_err": "Ошибка активации",
        "confirm_del": "Подтверждение", "ask_del": "Вы уверены, что хотите удалить этот элемент?"
    },
    "EN": {
        "title": "Grok Prompt Manager PRO", "tab_main": "💻 Prompt Database", "tab_admin": "⚙ Management",
        "tab_info": "📖 Information", "tab_help": "📝 Instruction", "nav": "🧭 NAVIGATION", "all_cats": "All Categories",
        "copy_btn": "🚀 COPY PROMPT", "save_btn": "💾 SAVE CHANGES", "del_btn": "🗑 DELETE ITEM",
        "add_new": "➕ ADD NEW PROMPT", "cat_label": "1. CATEGORY:", "name_label": "2. EFFECT NAME:",
        "desc_label": "3. DESCRIPTION (RU):", "prompt_label": "4. PROMPT (EN):", "lang_btn": "Язык: RU", "zoom_btn": "🔍 ZOOM",
        "about_btn": "ℹ ABOUT", "auth_title": "PROGRAM ACTIVATION", "auth_hwid": "Device ID:", "auth_copy_id": "📋 Copy ID",
        "auth_paste": "📥 PASTE", "auth_activate": "ACTIVATE", "auth_back": "↩ CHANGE LANGUAGE", "auth_err": "Activation Error",
        "confirm_del": "Confirmation", "ask_del": "Are you sure you want to delete this item?"
    }
}

class GrokPromptManager:
    def __init__(self, root):
        self.root = root
        self.current_lang = "RU"
        self.zoom_scale = 1.0
        self.root.configure(bg=BG_MAIN)
        self.base_dir = get_base_path()
        self.lic_file = os.path.join(self.base_dir, "grok_license.dat")
        self.user_data_file = os.path.join(self.base_dir, "user_grok_prompts.dat")
        self.hwid = hashlib.md5(str(uuid.getnode()).encode()).hexdigest()[:12].upper()
        
        self.prompts, self.categories_data = [], {}
        self.cur_adm_idx = None
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        self.show_language_selection()

    def apply_base_style(self):
        s = self.zoom_scale
        f_main = int(16 * s)
        f_tabs = int(13 * s)
        self.style.configure('TNotebook', background=BG_MAIN, borderwidth=0)
        self.style.configure('TNotebook.Tab', background=BG_PANEL, foreground=TEXT_MUTED, padding=[int(45*s), int(18*s)], font=('Segoe UI Bold', f_tabs))
        self.style.map('TNotebook.Tab', background=[('selected', ACCENT_2)], foreground=[('selected', '#ffffff')])
        self.style.configure('TCombobox', font=('Segoe UI Bold', f_main))
        self.root.option_add('*TCombobox*Listbox.font', ('Segoe UI Bold', f_main))

    def apply_zoom(self, scale):
        self.zoom_scale = scale
        w, h = int(1200 * scale), int(800 * scale)
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.apply_base_style()
        self.show_main_interface()

    def show_language_selection(self):
        for widget in self.root.winfo_children(): widget.destroy()
        self.root.geometry("1200x800")
        c = tk.Frame(self.root, bg=BG_MAIN); c.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(c, text="SELECT LANGUAGE / ВЫБЕРИТЕ ЯЗЫК", font=("Segoe UI Black", 24), bg=BG_MAIN, fg=ACCENT).pack(pady=40)
        tk.Button(c, text="РУССКИЙ ЯЗЫК", bg=ACCENT_2, fg="white", font=("Segoe UI Bold", 18), padx=40, pady=20, command=lambda: self.set_initial_lang("RU")).pack(pady=10, fill="x")
        tk.Button(c, text="ENGLISH LANGUAGE", bg="#444", fg="white", font=("Segoe UI Bold", 18), padx=40, pady=20, command=lambda: self.set_initial_lang("EN")).pack(pady=10, fill="x")

    def set_initial_lang(self, lang):
        self.current_lang = lang
        self.apply_base_style()
        if not self.check_license(): self.show_auth_window()
        else: self.show_main_interface()

    def check_license(self):
        if not os.path.exists(self.lic_file): return False
        try:
            with open(self.lic_file, "r") as f:
                return f.read().strip() == hashlib.sha256((self.hwid + SECRET_SALT).encode()).hexdigest()[:16].upper()
        except: return False

    def init_database(self):
        self.prompts = []
        self.categories_data = {}
        files = [f for f in os.listdir(self.base_dir) if f.endswith(".dat") and "grok_prompts" in f]
        for f_name in files:
            try:
                with open(os.path.join(self.base_dir, f_name), 'rb') as f:
                    raw = base64.b64decode(f.read())
                    dec = bytes([b ^ ord(SECRET_SALT[i % len(SECRET_SALT)]) for i, b in enumerate(raw)]).decode('utf-8')
                    batch = json.loads(dec)
                    for it in batch:
                        it["_source"] = "user" if "user" in f_name else "system"
                        self.prompts.append(it)
                        ru = it.get("category", "Общее")
                        if ru not in self.categories_data: self.categories_data[ru] = it.get("category_en", ru)
            except: pass
        if not self.categories_data: self.categories_data["Общее"] = "General"

    def show_main_interface(self, tab_index=0):
        s = self.zoom_scale
        for w in self.root.winfo_children(): w.destroy()
        self.init_database()
        l = LANG_DATA[self.current_lang]
        self.root.title(l["title"])
        header = tk.Frame(self.root, bg=BG_PANEL, pady=int(10*s)); header.pack(fill="x")
        tk.Label(header, text="🧠 Grok Prompt Manager", font=("Segoe UI Black", int(26*s)), bg=BG_PANEL, fg=ACCENT).pack(side="left", padx=int(30*s))
        
        tk.Button(header, text=l["about_btn"], bg="#333", fg="white", font=("Segoe UI Bold", int(10*s)), 
                  command=lambda: messagebox.showinfo(l["about_btn"], (ABOUT_RU if self.current_lang=="RU" else ABOUT_EN).format(hwid=self.hwid))).pack(side="right", padx=int(10*s))
        
        tk.Button(header, text=l["lang_btn"], bg=ACCENT_2, fg="white", font=("Segoe UI Bold", int(10*s)), command=self.toggle_lang).pack(side="right", padx=int(5*s))
        zm = tk.Menubutton(header, text=l["zoom_btn"], bg="#444", fg="white", font=("Segoe UI Bold", int(10*s)), relief="flat")
        zm.menu = tk.Menu(zm, tearoff=0, bg=BG_PANEL, fg="white", font=("Segoe UI", 12))
        zm["menu"] = zm.menu
        zm.menu.add_command(label="100%", command=lambda: self.apply_zoom(1.0)); zm.menu.add_command(label="75%", command=lambda: self.apply_zoom(0.75)); zm.menu.add_command(label="50%", command=lambda: self.apply_zoom(0.5))
        zm.pack(side="right", padx=int(5*s))

        self.nb = ttk.Notebook(self.root); self.nb.pack(fill="both", expand=True, padx=int(15*s), pady=int(10*s))
        t1, t2, t3, t4 = tk.Frame(self.nb, bg=BG_MAIN), tk.Frame(self.nb, bg=BG_MAIN), tk.Frame(self.nb, bg=BG_MAIN), tk.Frame(self.nb, bg=BG_MAIN)
        self.nb.add(t1, text=l["tab_main"]); self.nb.add(t2, text=l["tab_admin"]); self.nb.add(t3, text=l["tab_info"]); self.nb.add(t4, text=l["tab_help"])
        
        # TAB 1
        left = tk.Frame(t1, bg=BG_MAIN, width=int(350*s)); left.pack(side="left", fill="y", padx=(0, int(20*s)), pady=int(10*s)); left.pack_propagate(False)
        tk.Label(left, text=l["nav"], font=("Segoe UI Bold", int(15*s)), bg=BG_PANEL, fg=TEXT_MAIN).pack(fill="x", pady=(0, int(10*s)), ipady=int(18*s))
        self.cat_var = tk.StringVar(value=l["all_cats"])
        self.main_cb = ttk.Combobox(left, textvariable=self.cat_var, font=("Segoe UI Bold", int(16*s)), state="readonly", justify="center")
        self.main_cb.pack(fill="x", pady=(0, int(10*s)), ipady=int(12*s))
        self.main_cb.bind("<<ComboboxSelected>>", lambda e: self.update_list())
        
        cats = [l["all_cats"]] + sorted([c if self.current_lang == "RU" else self.categories_data[c] for c in self.categories_data.keys()])
        self.main_cb['values'] = cats

        self.listbox = tk.Listbox(left, bg=BG_PANEL, fg=TEXT_MAIN, bd=0, font=("Segoe UI Bold", int(16*s)), selectbackground=ACCENT, highlightthickness=0); self.listbox.pack(fill="both", expand=True); self.listbox.bind("<<ListboxSelect>>", self.on_select)
        right = tk.Frame(t1, bg=BG_PANEL, padx=int(30*s), pady=int(20*s)); right.pack(side="right", fill="both", expand=True, pady=int(10*s))
        self.btn_copy = tk.Button(right, text=l["copy_btn"], bg=ACCENT, fg="black", font=("Segoe UI Bold", int(18*s)), relief="flat", pady=int(22*s), command=self.copy_p); self.btn_copy.pack(side="bottom", fill="x")
        self.lbl_p_n = tk.Label(right, text="", font=("Segoe UI Black", int(24*s)), bg=BG_PANEL, fg=TEXT_MAIN, anchor="nw", wraplength=int(750*s), justify="left"); self.lbl_p_n.pack(fill="x", pady=(0, int(10*s)))
        self.txt_desc_main = tk.Text(right, bg=BG_PANEL, fg=TEXT_MAIN, font=("Segoe UI", int(16*s)), bd=0, wrap="word", height=5, state="disabled"); self.txt_desc_main.pack(fill="x", pady=(int(5*s), int(15*s)))
        self.txt_p_main = scrolledtext.ScrolledText(right, bg="#000000", fg=TEXT_MAIN, font=("Consolas", int(16*s)), bd=0, padx=int(15*s), pady=int(15*s), state="disabled"); self.txt_p_main.pack(fill="both", expand=True)

        # TAB 2
        f2 = tk.Frame(t2, bg=BG_MAIN, padx=int(20*s), pady=int(10*s)); f2.pack(fill="both", expand=True)
        la = tk.Frame(f2, bg=BG_MAIN, width=int(350*s)); la.pack(side="left", fill="y", padx=(0, int(15*s))); la.pack_propagate(False)
        self.afv = tk.StringVar(value=l["all_cats"])
        self.afc = ttk.Combobox(la, textvariable=self.afv, font=("Segoe UI Bold", int(16*s)), state="readonly", justify="center")
        self.afc.pack(fill="x", pady=5, ipady=int(10*s)); self.afc.bind("<<ComboboxSelected>>", lambda e: self.update_admin_list())
        self.afc['values'] = cats
        self.alb = tk.Listbox(la, bg=BG_PANEL, fg="white", bd=0, font=("Segoe UI Bold", int(16*s)), selectbackground=ACCENT); self.alb.pack(fill="both", expand=True); self.alb.bind("<<ListboxSelect>>", self.on_admin_select)
        ra = tk.Frame(f2, bg=BG_PANEL, padx=int(25*s), pady=int(15*s)); ra.pack(side="right", fill="both", expand=True)
        self.b_d = tk.Button(ra, text=l["del_btn"], bg=DANGER, fg="white", font=("Segoe UI Bold", int(14*s)), pady=int(18*s), command=self.del_adm, relief="flat"); self.b_d.pack(side="bottom", fill="x")
        self.b_s = tk.Button(ra, text=l["save_btn"], bg=SUCCESS, font=("Segoe UI Bold", int(14*s)), pady=int(18*s), command=self.save_adm, relief="flat"); self.b_s.pack(side="bottom", fill="x", pady=(0, int(5*s)))
        
        tk.Label(ra, text=l["cat_label"], bg=BG_PANEL, fg=TEXT_MAIN, font=("Segoe UI Bold", int(14*s))).pack(anchor="w")
        cl = tk.Frame(ra, bg=BG_PANEL); cl.pack(fill="x", pady=2)
        self.ecc = ttk.Combobox(cl, font=("Segoe UI Bold", int(16*s)), state="readonly"); self.ecc.pack(side="left", fill="x", expand=True, ipady=int(10*s))
        self.ecc['values'] = sorted([c if self.current_lang == "RU" else self.categories_data[c] for c in self.categories_data.keys()])
        tk.Button(cl, text="+", bg=SUCCESS, width=5, font=("Segoe UI Bold", int(13*s)), command=self.add_cat).pack(side="left", padx=5); tk.Button(cl, text="-", bg=DANGER, fg="white", width=5, font=("Segoe UI Bold", int(13*s)), command=self.del_cat).pack(side="left")
        
        tk.Button(ra, text=l["add_new"], bg="#333", fg="white", font=("Segoe UI Bold", int(13*s)), pady=int(12*s), command=self.clear_adm, relief="flat").pack(fill="x", pady=(int(8*s), int(10*s)))
        tk.Label(ra, text=l["name_label"], bg=BG_PANEL, fg=TEXT_MAIN, font=("Segoe UI Bold", int(14*s))).pack(anchor="w")
        self.a_en = tk.Entry(ra, font=("Segoe UI Bold", int(15*s)), bg=BG_MAIN, fg="white", bd=0, insertbackground="white"); self.a_en.pack(fill="x", pady=2, ipady=12)
        tk.Label(ra, text=l["desc_label"], bg=BG_PANEL, fg=TEXT_MAIN, font=("Segoe UI Bold", int(14*s))).pack(anchor="w")
        self.a_rd = scrolledtext.ScrolledText(ra, height=3, font=("Segoe UI Semibold", int(14*s)), bg=BG_MAIN, fg="white", bd=0, wrap="word", insertbackground="white"); self.a_rd.pack(fill="x", pady=2)
        tk.Label(ra, text=l["prompt_label"], bg=BG_PANEL, fg=TEXT_MAIN, font=("Segoe UI Bold", int(14*s))).pack(anchor="w")
        self.a_tp = scrolledtext.ScrolledText(ra, height=10, font=("Consolas Bold", int(14*s)), bg=BG_MAIN, fg="white", bd=0, insertbackground="white"); self.a_tp.pack(fill="both", expand=True, pady=2)

        for t, txt in [(t3, INFO_RU if self.current_lang == "RU" else INFO_EN), (t4, HELP_RU if self.current_lang == "RU" else HELP_EN)]:
            st = scrolledtext.ScrolledText(t, font=("Segoe UI Semibold", int(15*s)), bg=BG_PANEL, fg=TEXT_MAIN, bd=0, padx=int(45*s), pady=int(45*s), wrap="word")
            st.pack(fill="both", expand=True, padx=int(15*s), pady=int(15*s)); st.insert("1.0", txt); st.config(state="disabled")
        
        self.nb.select(tab_index); self.update_list()

    def toggle_lang(self): self.current_lang = "EN" if self.current_lang == "RU" else "RU"; self.show_main_interface()
    def update_list(self):
        self.listbox.delete(0, tk.END); self.cur_map = []
        sel, all_l = self.cat_var.get(), LANG_DATA[self.current_lang]["all_cats"]
        for i, p in enumerate(self.prompts):
            disp = p.get('category', 'Общее') if self.current_lang == "RU" else p.get('category_en', p.get('category', 'Общее'))
            if sel == all_l or disp == sel: self.listbox.insert(tk.END, f" {p['name']}"); self.cur_map.append(i)
    def update_admin_list(self):
        self.alb.delete(0, tk.END); self.adm_map = []
        sel, all_l = self.afv.get(), LANG_DATA[self.current_lang]["all_cats"]
        for i, p in enumerate(self.prompts):
            disp = p.get('category', 'Общее') if self.current_lang == "RU" else p.get('category_en', p.get('category', 'Общее'))
            if sel == all_l or disp == sel: self.alb.insert(tk.END, f" {p['name']}"); self.adm_map.append(i)
    def on_select(self, e):
        if not self.listbox.curselection(): return
        item = self.prompts[self.cur_map[self.listbox.curselection()[0]]]; self.lbl_p_n.config(text=item['name'])
        d = item.get('desc_en', item.get('desc_ru', '')) if self.current_lang == "EN" else item.get('desc_ru', '')
        for w, t in [(self.txt_desc_main, d), (self.txt_p_main, item.get('prompt', ''))]:
            w.config(state="normal"); w.delete("1.0", tk.END); w.insert("1.0", t); w.config(state="disabled")
    def on_admin_select(self, e):
        if not self.alb.curselection(): return
        self.cur_adm_idx = self.adm_map[self.alb.curselection()[0]]; it = self.prompts[self.cur_adm_idx]
        st = "normal" if it.get("_source") == "user" else "disabled"
        self.b_s.config(state=st); self.b_d.config(state=st); self.ecc.set(it.get('category', 'Общее') if self.current_lang=="RU" else it.get('category_en', it.get('category', 'Общее')))
        self.a_en.delete(0, tk.END); self.a_en.insert(0, it['name']); self.a_tp.delete("1.0", tk.END); self.a_tp.insert("1.0", it['prompt']); self.a_rd.delete("1.0", tk.END); self.a_rd.insert("1.0", it.get('desc_ru', ''))
    def save_adm(self):
        c_disp, n = self.ecc.get(), self.a_en.get().strip()
        if not (c_disp and n): return
        ul = []
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'rb') as f:
                    raw = base64.b64decode(f.read())
                    dec = bytes([b ^ ord(SECRET_SALT[i % len(SECRET_SALT)]) for i, b in enumerate(raw)]).decode('utf-8')
                    ul = json.loads(dec)
            except: pass
        new = {"name": n, "category": c_disp, "category_en": c_disp, "prompt": self.a_tp.get("1.0", tk.END).strip(), "desc_ru": self.a_rd.get("1.0", tk.END).strip(), "_source": "user"}
        if self.cur_adm_idx is not None and self.prompts[self.cur_adm_idx].get("_source") == "user":
            on = self.prompts[self.cur_adm_idx]['name']
            for i, p in enumerate(ul):
                if p['name'] == on: ul[i] = new; break
        else: ul = [p for p in ul if p['name'] != n]; ul.append(new)
        open(self.user_data_file, 'wb').write(base64.b64encode(bytes([b ^ ord(SECRET_SALT[i % len(SECRET_SALT)]) for i, b in enumerate(json.dumps(ul, ensure_ascii=False).encode('utf-8'))])))
        self.show_main_interface(tab_index=1)
    def del_adm(self):
        l = LANG_DATA[self.current_lang]
        if self.cur_adm_idx is None or not messagebox.askyesno(l["confirm_del"], l["ask_del"]): return
        n = self.prompts[self.cur_adm_idx]['name']
        try:
            raw = base64.b64decode(open(self.user_data_file, 'rb').read())
            dec = bytes([b ^ ord(SECRET_SALT[i % len(SECRET_SALT)]) for i, b in enumerate(raw)]).decode('utf-8')
            ul = [p for p in json.loads(dec) if p['name'] != n]
            open(self.user_data_file, 'wb').write(base64.b64encode(bytes([b ^ ord(SECRET_SALT[i % len(SECRET_SALT)]) for i, b in enumerate(json.dumps(ul, ensure_ascii=False).encode('utf-8'))])))
            self.show_main_interface(tab_index=1)
        except: pass
    def add_cat(self):
        n = simpledialog.askstring("RU", "Название:")
        if n and n not in self.categories_data:
            self.categories_data[n] = n
            vals = [LANG_DATA[self.current_lang]["all_cats"]] + sorted([c if self.current_lang == "RU" else self.categories_data[c] for c in self.categories_data.keys()])
            self.main_cb['values'], self.afc['values'] = vals, vals
            self.ecc['values'] = sorted([c if self.current_lang == "RU" else self.categories_data[c] for c in self.categories_data.keys()])
            self.ecc.set(n)
    def del_cat(self):
        l = LANG_DATA[self.current_lang]; cd = self.ecc.get()
        if cd and messagebox.askyesno(l["confirm_del"], l["ask_del"]):
            try:
                raw = base64.b64decode(open(self.user_data_file, 'rb').read())
                dec = bytes([b ^ ord(SECRET_SALT[i % len(SECRET_SALT)]) for i, b in enumerate(raw)]).decode('utf-8')
                ul = [p for p in json.loads(dec) if p.get('category') != cd]
                open(self.user_data_file, 'wb').write(base64.b64encode(bytes([b ^ ord(SECRET_SALT[i % len(SECRET_SALT)]) for i, b in enumerate(json.dumps(ul, ensure_ascii=False).encode('utf-8'))])))
                if cd in self.categories_data: del self.categories_data[cd]
                self.show_main_interface(tab_index=1)
            except: pass
    def clear_adm(self): self.cur_adm_idx = None; self.a_en.delete(0, tk.END); self.a_tp.delete("1.0", tk.END); self.a_rd.delete("1.0", tk.END)
    def copy_p(self):
        c = self.txt_p_main.get("1.0", tk.END).strip()
        if c: self.root.clipboard_clear(); self.root.clipboard_append(c); messagebox.showinfo("OK", "Copied")
    def show_auth_window(self):
        for widget in self.root.winfo_children(): widget.destroy()
        l = LANG_DATA[self.current_lang]; c = tk.Frame(self.root, bg=BG_MAIN); c.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(c, text="🧠 Grok Prompt Manager", font=("Segoe UI Black", 42), bg=BG_MAIN, fg=ACCENT).pack()
        idf = tk.Frame(c, bg=BG_MAIN, pady=10); idf.pack()
        tk.Label(idf, text=f"{l['auth_hwid']} {self.hwid}", bg=BG_MAIN, fg=TEXT_MUTED, font=("Consolas Bold", 14)).pack(side="left", padx=15)
        tk.Button(idf, text=l['auth_copy_id'], bg="#333", fg="white", font=("Segoe UI Bold", 10), command=lambda: (self.root.clipboard_clear(), self.root.clipboard_append(self.hwid), messagebox.showinfo("OK", "ID Copied!"))).pack(side="left")
        tk.Button(c, text=l['auth_paste'], bg="#444", fg="white", font=("Segoe UI Bold", 12), command=lambda: (self.ki.delete(0, tk.END), self.ki.insert(0, self.root.clipboard_get()))).pack(pady=5)
        self.ki = tk.Entry(c, font=("Consolas", 22), justify="center", bg=BG_PANEL, fg="white", width=25, insertbackground="white"); self.ki.pack(pady=10, ipady=10)
        tk.Button(c, text=l['auth_activate'], bg=ACCENT, fg="black", font=("Segoe UI Bold", 16), padx=50, pady=20, command=lambda: self.activate_now(self.ki.get().strip().upper())).pack(pady=15)
        tk.Button(c, text=l['auth_back'], bg=DANGER, fg="white", font=("Segoe UI Bold", 10), command=self.show_language_selection).pack(pady=10)
    def activate_now(self, k):
        if k == hashlib.sha256((self.hwid + SECRET_SALT).encode()).hexdigest()[:16].upper():
            open(self.lic_file, "w").write(k); self.show_main_interface()
        else: messagebox.showerror("X", LANG_DATA[self.current_lang]['auth_err'])

if __name__ == "__main__":
    root = tk.Tk(); app = GrokPromptManager(root); root.mainloop()