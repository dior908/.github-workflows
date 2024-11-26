import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import hashlib
import os
import pystray
from PIL import Image, ImageDraw
from datetime import datetime
from tkcalendar import DateEntry
import folium
from tkinterweb import HtmlFrame
import telebot
from pywhatkit import sendwhatmsg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_data(file_name):
    if not os.path.exists(file_name):
        return {}
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

class MedRepApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Контроль медицинских представителей")
        self.users_file = 'users.json'
        self.visits_file = 'visits.json'
        self.access_code = "12051993"
        self.user = None

        self.show_login_window()

    def show_login_window(self):
        self.root.geometry("400x400")
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Добро пожаловать в программу контроля!", font=("Arial", 14), pady=10).pack()

        tk.Label(self.root, text="Логин:").pack(anchor="w", padx=10)
        self.login_entry = tk.Entry(self.root)
        self.login_entry.pack(fill="x", padx=10)

        tk.Label(self.root, text="Пароль:").pack(anchor="w", padx=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(fill="x", padx=10)

        self.remember_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Запомнить", variable=self.remember_var).pack(anchor="w", padx=10)

        tk.Button(self.root, text="Войти", bg="blue", fg="white", command=self.login_user).pack(pady=10)
        tk.Button(self.root, text="Зарегистрироваться", command=self.show_registration_window).pack()
        tk.Button(self.root, text="Скрыть в трей", command=self.hide_to_tray).pack(pady=10)

        self.root.mainloop()

    def login_user(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if not login or not password:
            messagebox.showwarning("Ошибка", "Все поля должны быть заполнены.")
            return

        users = load_data(self.users_file)
        if login not in users or users[login]["password"] != hash_password(password):
            messagebox.showwarning("Ошибка", "Неверный логин или пароль.")
            return

        self.user = users[login]
        self.user['login'] = login  # Сохраняем имя пользователя для дальнейшей работы
        messagebox.showinfo("Успех", f"Добро пожаловать, {login}!")
        self.show_main_window()

    def show_registration_window(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Регистрация")
        reg_window.geometry("400x500")

        tk.Label(reg_window, text="Введите ваше имя:", anchor="w").pack(pady=5, fill="x")
        name_entry = tk.Entry(reg_window)
        name_entry.pack(pady=5, fill="x")

        tk.Label(reg_window, text="Введите пароль:", anchor="w").pack(pady=5, fill="x")
        password_entry = tk.Entry(reg_window, show="*")
        password_entry.pack(pady=5, fill="x")

        tk.Label(reg_window, text="Повторите пароль:", anchor="w").pack(pady=5, fill="x")
        confirm_password_entry = tk.Entry(reg_window, show="*")
        confirm_password_entry.pack(pady=5, fill="x")

        tk.Label(reg_window, text="Код доступа:", anchor="w").pack(pady=5, fill="x")
        code_entry = tk.Entry(reg_window)
        code_entry.pack(pady=5, fill="x")

        tk.Label(reg_window, text="Регион:", anchor="w").pack(pady=5, fill="x")
        region_var = tk.StringVar()
        regions = [
            "Андижанская область", "Бухарская область", "Джизакская область",
            "Кашкадарьинская область", "Навоийская область", "Наманганская область",
            "Самаркандская область", "Сурхандарьинская область", "Сырдарьинская область",
            "Ташкентская область", "Ферганская область", "Хорезмская область",
            "Республика Каракалпакстан", "г. Ташкент"
        ]
        region_combobox = ttk.Combobox(reg_window, textvariable=region_var, values=regions, state="readonly")
        region_combobox.pack(pady=5, fill="x")

        tk.Label(reg_window, text="E-mail (по желанию):", anchor="w").pack(pady=5, fill="x")
        email_entry = tk.Entry(reg_window)
        email_entry.pack(pady=5, fill="x")

        def register_user():
            name = name_entry.get().strip()
            password = password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()
            code = code_entry.get().strip()
            region = region_var.get()
            email = email_entry.get().strip()

            if not name or not password or not confirm_password or not code or not region:
                messagebox.showwarning("Ошибка", "Все обязательные поля должны быть заполнены.")
                return

            if password != confirm_password:
                messagebox.showwarning("Ошибка", "Пароли не совпадают.")
                return

            if code != self.access_code:
                messagebox.showwarning("Ошибка", "Неверный код доступа.")
                return

            users = load_data(self.users_file)
            if name in users:
                messagebox.showwarning("Ошибка", "Пользователь с таким именем уже существует.")
                return

            users[name] = {
                "password": hash_password(password),
                "region": region,
                "email": email
            }
            save_data(self.users_file, users)
            messagebox.showinfo("Успех", "Регистрация прошла успешно.")
            reg_window.destroy()

        tk.Button(reg_window, text="Зарегистрироваться", command=register_user, bg="blue", fg="white").pack(pady=20)

    def show_main_window(self):
        self.root.geometry("400x400")
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Добро пожаловать, {self.user['login']}!", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Просмотр профиля", command=self.show_profile).pack(pady=5)
        tk.Button(self.root, text="Форма визита", command=self.show_visit_form).pack(pady=5)
        tk.Button(self.root, text="Отчет по посещениям", command=self.show_visit_report).pack(pady=5)
        tk.Button(self.root, text="Статистика задач", command=self.show_task_statistics).pack(pady=5)
        tk.Button(self.root, text="Выход", command=self.root.destroy, bg="red", fg="white").pack(pady=20)

    def show_profile(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Профиль пользователя")
        profile_window.geometry("400x300")

        tk.Label(profile_window, text=f"Имя: {self.user['login']}", font=("Arial", 12)).pack(pady=5)
        tk.Label(profile_window, text=f"Регион: {self.user['region']}", font=("Arial", 12)).pack(pady=5)
        tk.Label(profile_window, text=f"E-mail: {self.user.get('email', 'Не указан')}", font=("Arial", 12)).pack(pady=5)

        def edit_profile():
            edit_window = tk.Toplevel(profile_window)
            edit_window.title("Редактирование профиля")
            edit_window.geometry("400x400")

            tk.Label(edit_window, text="Имя:").pack(anchor="w", padx=10)
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, self.user['login'])
            name_entry.pack(fill="x", padx=10, pady=5)

            tk.Label(edit_window, text="Пароль:").pack(anchor="w", padx=10)
            password_entry = tk.Entry(edit_window, show="*")
            password_entry.pack(fill="x", padx=10, pady=5)

            tk.Label(edit_window, text="Повторите пароль:").pack(anchor="w", padx=10)
            confirm_password_entry = tk.Entry(edit_window, show="*")
            confirm_password_entry.pack(fill="x", padx=10, pady=5)

            tk.Label(edit_window, text="E-mail:").pack(anchor="w", padx=10)
            email_entry = tk.Entry(edit_window)
            email_entry.insert(0, self.user.get('email', ''))
            email_entry.pack(fill="x", padx=10, pady=5)

            region_var = tk.StringVar(value=self.user['region'])
            tk.Label(edit_window, text="Регион:").pack(anchor="w", padx=10)
            regions = [
                "Андижанская область", "Бухарская область", "Джизакская область",
                "Кашкадарьинская область", "Навоийская область", "Наманганская область",
                "Самаркандская область", "Сурхандарьинская область", "Сырдарьинская область",
                "Ташкентская область", "Ферганская область", "Хорезмская область",
                "Республика Каракалпакстан", "г. Ташкент"
            ]
            region_combobox = ttk.Combobox(edit_window, textvariable=region_var, values=regions, state="readonly")
            region_combobox.set(self.user['region'])
            region_combobox.pack(fill="x", padx=10, pady=5)

            def save_changes():
                self.user['login'] = name_entry.get()
                self.user['region'] = region_var.get()
                self.user['email'] = email_entry.get()

                password = password_entry.get()
                if password:
                    self.user['password'] = hash_password(password)

                save_data(self.users_file, {self.user['login']: self.user})
                messagebox.showinfo("Успех", "Данные успешно изменены.")
                edit_window.destroy()

            tk.Button(edit_window, text="Сохранить изменения", command=save_changes, bg="blue", fg="white").pack(pady=10)

        tk.Button(profile_window, text="Изменить данные", command=edit_profile).pack(pady=10)

    def show_visit_form(self):
        visit_window = tk.Toplevel(self.root)
        visit_window.title("Форма визита")
        visit_window.geometry("400x600")

        tk.Label(visit_window, text="Форма визита", font=("Arial", 14)).pack(pady=10)

        tk.Label(visit_window, text="Дата визита:").pack(anchor="w", padx=10)
        date_frame = tk.Frame(visit_window)
        date_frame.pack(fill="x", padx=10, pady=5)

        day_var = tk.StringVar(value=datetime.now().day)
        month_var = tk.StringVar(value=datetime.now().month)
        year_var = tk.StringVar(value=datetime.now().year)

        day_spinbox = tk.Spinbox(date_frame, from_=1, to=31, textvariable=day_var, width=5)
        day_spinbox.pack(side="left", padx=5)
        month_spinbox = tk.Spinbox(date_frame, from_=1, to=12, textvariable=month_var, width=5)
        month_spinbox.pack(side="left", padx=5)
        year_spinbox = tk.Spinbox(date_frame, from_=2000, to=2030, textvariable=year_var, width=5)
        year_spinbox.pack(side="left", padx=5)

        tk.Label(visit_window, text="Вид деятельности:").pack(anchor="w", padx=10)
        activity_var = tk.StringVar()
        activity_combobox = ttk.Combobox(visit_window, textvariable=activity_var, values=["Аптека", "Врач", "Оптовик"], state="readonly")
        activity_combobox.pack(fill="x", padx=10, pady=5)

        def show_help():
            help_window = tk.Toplevel(visit_window)
            help_window.title("Помощь")
            help_window.geometry("300x200")
            help_text = ""
            if activity_var.get() == "Аптека":
                help_text = "Введите юридическое название аптеки и контактное лицо."
            elif activity_var.get() == "Врач":
                help_text = "Введите специализацию врача и его должность."
            elif activity_var.get() == "Оптовик":
                help_text = "Введите название оптовика и контактное лицо."
            tk.Label(help_window, text=help_text, wraplength=250).pack(pady=10)

        tk.Button(visit_window, text="?", command=show_help).pack(anchor="e", padx=10)

        tk.Label(visit_window, text="Название:").pack(anchor="w", padx=10)
        name_entry = tk.Entry(visit_window)
        name_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(visit_window, text="Контактное лицо/Специализация:").pack(anchor="w", padx=10)
        contact_entry = tk.Entry(visit_window)
        contact_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(visit_window, text="Название препарата:").pack(anchor="w", padx=10)
        drug_entry = tk.Entry(visit_window)
        drug_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(visit_window, text="Краткий итог визита:").pack(anchor="w", padx=10)
        summary_entry = tk.Text(visit_window, height=5)
        summary_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(visit_window, text="Локация местонахождения:").pack(anchor="w", padx=10)
        location_entry = tk.Entry(visit_window)
        location_entry.pack(fill="x", padx=10, pady=5)

        def show_map():
            map_window = tk.Toplevel(visit_window)
            map_window.title("Карта местонахождения")
            map_window.geometry("600x400")

            frame = HtmlFrame(map_window)
            frame.pack(fill="both", expand=True)

            # Создаем карту с помощью folium
            m = folium.Map(location=[41.3111, 69.2406], zoom_start=13)
            folium.Marker([41.3111, 69.2406], popup="Местонахождение").add_to(m)

            # Сохраняем карту в HTML файл
            map_html = "map.html"
            m.save(map_html)

            # Отображаем карту в HtmlFrame
            frame.load_file(map_html)

            def save_location():
                location_entry.insert(0, "41.3111, 69.2406")
                map_window.destroy()

            tk.Button(map_window, text="Сохранить", command=save_location).pack(pady=10)

        tk.Button(visit_window, text="Показать карту", command=show_map).pack(pady=5)

        tk.Label(visit_window, text="Телефон:").pack(anchor="w", padx=10)
        phone_entry = tk.Entry(visit_window)
        phone_entry.pack(fill="x", padx=10, pady=5)

        def save_visit():
            date = f"{year_var.get()}-{month_var.get().zfill(2)}-{day_var.get().zfill(2)}"
            activity = activity_var.get()
            name = name_entry.get().strip()
            contact = contact_entry.get().strip()
            drug = drug_entry.get().strip()
            summary = summary_entry.get("1.0", tk.END).strip()
            location = location_entry.get().strip()
            phone = phone_entry.get().strip()

            if not date or not activity or not name or not contact or not drug or not summary or not location or not phone:
                messagebox.showwarning("Ошибка", "Все поля должны быть заполнены.")
                return

            visits = load_data(self.visits_file)
            visit_id = len(visits) + 1
            visits[visit_id] = {
                "date": date,
                "activity": activity,
                "name": name,
                "contact": contact,
                "drug": drug,
                "summary": summary,
                "location": location,
                "phone": phone
            }
            save_data(self.visits_file, visits)
            messagebox.showinfo("Успех", "Визит успешно сохранен.")
            visit_window.destroy()

        tk.Button(visit_window, text="Сохранить визит", command=save_visit, bg="blue", fg="white").pack(pady=10)

    def show_visit_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Отчет по посещениям")
        report_window.geometry("600x400")

        tk.Label(report_window, text="Отчет по посещениям", font=("Arial", 14)).pack(pady=10)

        tk.Label(report_window, text="Выберите дату:").pack(anchor="w", padx=10)
        date_frame = tk.Frame(report_window)
        date_frame.pack(fill="x", padx=10, pady=5)

        day_var = tk.StringVar(value=datetime.now().day)
        month_var = tk.StringVar(value=datetime.now().month)
        year_var = tk.StringVar(value=datetime.now().year)

        day_spinbox = tk.Spinbox(date_frame, from_=1, to=31, textvariable=day_var, width=5)
        day_spinbox.pack(side="left", padx=5)
        month_spinbox = tk.Spinbox(date_frame, from_=1, to=12, textvariable=month_var, width=5)
        month_spinbox.pack(side="left", padx=5)
        year_spinbox = tk.Spinbox(date_frame, from_=2000, to=2030, textvariable=year_var, width=5)
        year_spinbox.pack(side="left", padx=5)

        def filter_visits():
            selected_date = f"{year_var.get()}-{month_var.get().zfill(2)}-{day_var.get().zfill(2)}"
            visits = load_data(self.visits_file)
            filtered_visits = {visit_id: visit for visit_id, visit in visits.items() if visit.get('date') == selected_date}

            report_text.config(state=tk.NORMAL)
            report_text.delete(1.0, tk.END)

            if not filtered_visits:
                report_text.insert(tk.END, "Нет данных для отображения.")
            else:
                for visit_id, visit in filtered_visits.items():
                    report_text.insert(tk.END, f"Визит {visit_id}:\n")
                    report_text.insert(tk.END, f"Дата: {visit.get('date', 'Не указано')}\n")
                    report_text.insert(tk.END, f"Вид деятельности: {visit.get('activity', 'Не указано')}\n")
                    report_text.insert(tk.END, f"Название: {visit.get('name', 'Не указано')}\n")
                    report_text.insert(tk.END, f"Контактное лицо/Специализация: {visit.get('contact', 'Не указано')}\n")
                    report_text.insert(tk.END, f"Название препарата: {visit.get('drug', 'Не указано')}\n")
                    if 'summary' in visit:
                        report_text.insert(tk.END, f"Краткий итог визита: {visit['summary']}\n")
                    report_text.insert(tk.END, f"Локация местонахождения: {visit.get('location', 'Не указано')}\n")
                    report_text.insert(tk.END, f"Телефон: {visit.get('phone', 'Не указано')}\n")
                    report_text.insert(tk.END, "\n")

            report_text.config(state=tk.DISABLED)

        tk.Button(report_window, text="Фильтровать", command=filter_visits).pack(pady=5)

        report_text = tk.Text(report_window, wrap="word")
        report_text.pack(fill="both", expand=True, padx=10, pady=10)

        def send_report():
            selected_date = f"{year_var.get()}-{month_var.get().zfill(2)}-{day_var.get().zfill(2)}"
            visits = load_data(self.visits_file)
            filtered_visits = {visit_id: visit for visit_id, visit in visits.items() if visit.get('date') == selected_date}

            if not filtered_visits:
                messagebox.showwarning("Ошибка", "Нет данных для отправки.")
                return

            report_content = ""
            for visit_id, visit in filtered_visits.items():
                report_content += f"Визит {visit_id}:\n"
                report_content += f"Дата: {visit.get('date', 'Не указано')}\n"
                report_content += f"Вид деятельности: {visit.get('activity', 'Не указано')}\n"
                report_content += f"Название: {visit.get('name', 'Не указано')}\n"
                report_content += f"Контактное лицо/Специализация: {visit.get('contact', 'Не указано')}\n"
                report_content += f"Название препарата: {visit.get('drug', 'Не указано')}\n"
                if 'summary' in visit:
                    report_content += f"Краткий итог визита: {visit['summary']}\n"
                report_content += f"Локация местонахождения: {visit.get('location', 'Не указано')}\n"
                report_content += f"Телефон: {visit.get('phone', 'Не указано')}\n"
                report_content += "\n"

            # Отправка отчета в Telegram
            telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
            chat_id = "YOUR_CHAT_ID"
            bot = telebot.TeleBot(telegram_token)
            try:
                bot.send_message(chat_id, report_content)
                messagebox.showinfo("Успех", "Отчет успешно отправлен в Telegram.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось отправить отчет в Telegram: {e}")

            # Отправка отчета в WhatsApp
            phone_number = "RECIPIENT_PHONE_NUMBER"
            try:
                sendwhatmsg(phone_number, report_content, datetime.now().hour, datetime.now().minute + 1)
                messagebox.showinfo("Успех", "Отчет успешно отправлен в WhatsApp.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось отправить отчет в WhatsApp: {e}")

        tk.Button(report_window, text="Отправить отчет", command=send_report).pack(pady=5)

    def show_task_statistics(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика задач")
        stats_window.geometry("600x400")

        tk.Label(stats_window, text="Статистика задач", font=("Arial", 14)).pack(pady=10)

        visits = load_data(self.visits_file)
        dates = [visit['date'] for visit in visits.values()]
        unique_dates = sorted(set(dates), key=lambda x: datetime.strptime(x, "%Y-%m-%d"))

        doctor_visits = [visit for visit in visits.values() if visit['activity'] == "Врач"]
        pharmacy_visits = [visit for visit in visits.values() if visit['activity'] == "Аптека"]

        doctor_counts = [len([visit for visit in doctor_visits if visit['date'] == date]) for date in unique_dates]
        pharmacy_counts = [len([visit for visit in pharmacy_visits if visit['date'] == date]) for date in unique_dates]

        fig, ax = plt.subplots()
        ax.plot(unique_dates, doctor_counts, label="Врачи")
        ax.plot(unique_dates, pharmacy_counts, label="Аптеки")
        ax.axhline(y=7, color='r', linestyle='--', label="Норма для врачей (7-12)")
        ax.axhline(y=12, color='r', linestyle='--')
        ax.axhline(y=6, color='b', linestyle='--', label="Норма для аптек (6-10)")
        ax.axhline(y=10, color='b', linestyle='--')
        ax.set_xlabel("Дата")
        ax.set_ylabel("Количество визитов")
        ax.set_title("Статистика визитов")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def hide_to_tray(self):
        self.root.withdraw()
        image = Image.new("RGB", (64, 64), "white")
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            [(16, 16), (48, 48)],
            fill="black",
        )
        icon = pystray.Icon("name", image, "MedRepApp", self.create_tray_menu())
        icon.run()

    def create_tray_menu(self):
        menu = pystray.Menu(
            pystray.MenuItem('Показать', self.show_window),
            pystray.MenuItem('Выход', self.exit_app)
        )
        return menu

    def show_window(self, icon, item):
        self.root.deiconify()
        icon.stop()

    def exit_app(self, icon, item):
        self.root.destroy()

if __name__ == "__main__":
    app = MedRepApp()
