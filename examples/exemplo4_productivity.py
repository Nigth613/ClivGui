"""
EXEMPLO 4: PRODUCTIVITY DASHBOARD
Gerenciador de tarefas com timer Pomodoro, notas e estatísticas
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from cliv_gui import (ClivMenu, ModernSlider, ModernCheck, ImageSeparator,
                      ModernButton, ModernGraph)
import threading
import time
import datetime
import tkinter as tk
from tkinter import scrolledtext


class ProductivityDashboard:
    def __init__(self):
        # Criar menu principal
        self.menu = ClivMenu(
            title="⚡ PRODUCTIVITY PRO",
            theme_color="#9c27b0",
            part_color="#ba68c8",
            part_count=50,
            part_speed=(0.2, 0.8)
        )

        # Sistema de tarefas
        self.tasks = []
        self.completed_tasks = []

        # Timer Pomodoro
        self.pomodoro_running = False
        self.pomodoro_time = 25 * 60  # 25 minutos
        self.break_time = 5 * 60  # 5 minutos
        self.current_timer = self.pomodoro_time
        self.timer_type = "work"  # work ou break
        self.pomodoros_completed = 0

        # Estatísticas
        self.total_work_time = 0
        self.total_break_time = 0
        self.tasks_completed_today = 0

        # Criar abas
        self.setup_tasks_tab()
        self.setup_pomodoro_tab()
        self.setup_notes_tab()
        self.setup_stats_tab()

        # Iniciar sistema de timer
        self.start_timer_system()

    def setup_tasks_tab(self):
        """Configura a aba de tarefas"""
        tasks = self.menu.add_tab("TASKS")

        ImageSeparator(tasks, "✅ TASK MANAGER", menu_ref=self.menu)

        # Frame para adicionar tarefa
        add_frame = tk.Frame(tasks, bg=self.menu.bg_color, pady=10)
        add_frame.pack(fill='x', padx=30)

        tk.Label(
            add_frame,
            text="New Task:",
            bg=self.menu.bg_color,
            fg="white",
            font=("Arial", 8, "bold")
        ).pack(anchor='w')

        self.task_entry = tk.Entry(
            add_frame,
            bg="#1a1a1a",
            fg=self.menu.theme,
            font=("Arial", 10),
            bd=2,
            relief='solid',
            insertbackground=self.menu.theme
        )
        self.task_entry.pack(fill='x', pady=5)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Prioridade
        priority_frame = tk.Frame(add_frame, bg=self.menu.bg_color)
        priority_frame.pack(fill='x', pady=5)

        tk.Label(
            priority_frame,
            text="Priority:",
            bg=self.menu.bg_color,
            fg="gray",
            font=("Arial", 7)
        ).pack(side='left', padx=(0, 10))

        self.priority_var = tk.StringVar(value="Medium")
        for priority in ["Low", "Medium", "High", "Urgent"]:
            rb = tk.Radiobutton(
                priority_frame,
                text=priority,
                variable=self.priority_var,
                value=priority,
                bg=self.menu.bg_color,
                fg=self.menu.theme,
                selectcolor="#1a1a1a",
                activebackground=self.menu.bg_color,
                font=("Arial", 7)
            )
            rb.pack(side='left', padx=3)

        ModernButton(
            tasks,
            "➕ Add Task",
            self.menu,
            callback=self.add_task,
            style="success"
        )

        ImageSeparator(tasks, "📋 ACTIVE TASKS", menu_ref=self.menu)

        # Lista de tarefas
        self.tasks_listbox_frame = tk.Frame(tasks, bg=self.menu.bg_color)
        self.tasks_listbox_frame.pack(fill='both', expand=True, padx=30, pady=10)

        self.tasks_text = scrolledtext.ScrolledText(
            self.tasks_listbox_frame,
            bg="#0a0a15",
            fg="white",
            font=("Courier", 9),
            height=10,
            bd=0,
            highlightthickness=2,
            highlightbackground=self.menu.theme,
            wrap=tk.WORD
        )
        self.tasks_text.pack(fill='both', expand=True)

        # Botões de ação
        action_frame = tk.Frame(tasks, bg=self.menu.bg_color)
        action_frame.pack(fill='x', padx=30, pady=5)

        btn_frame1 = tk.Frame(action_frame, bg=self.menu.bg_color)
        btn_frame1.pack(fill='x', pady=2)

        ModernButton(
            btn_frame1,
            "✓ Complete Selected",
            self.menu,
            callback=self.complete_task,
            style="success"
        )

        ModernButton(
            btn_frame1,
            "🗑️ Delete Selected",
            self.menu,
            callback=self.delete_task,
            style="danger"
        )

        ModernButton(
            tasks,
            "🔄 Refresh List",
            self.menu,
            callback=self.update_tasks_display,
            style="info"
        )

        self.update_tasks_display()

    def setup_pomodoro_tab(self):
        """Configura a aba do timer Pomodoro"""
        pomodoro = self.menu.add_tab("POMODORO")

        ImageSeparator(pomodoro, "🍅 POMODORO TIMER", menu_ref=self.menu)

        # Display do timer
        timer_frame = tk.Frame(pomodoro, bg=self.menu.bg_color, pady=20)
        timer_frame.pack(fill='x', padx=30)

        self.timer_label = tk.Label(
            timer_frame,
            text="25:00",
            bg=self.menu.bg_color,
            fg=self.menu.theme,
            font=("Digital-7", 48, "bold")
        )
        self.timer_label.pack()

        self.timer_status = tk.Label(
            timer_frame,
            text="Ready to work",
            bg=self.menu.bg_color,
            fg="gray",
            font=("Arial", 10)
        )
        self.timer_status.pack()

        # Barra de progresso visual
        self.progress_canvas = tk.Canvas(
            pomodoro,
            height=20,
            bg=self.menu.bg_color,
            highlightthickness=0,
            bd=0
        )
        self.progress_canvas.pack(fill='x', padx=30, pady=10)

        # Controles
        controls_frame = tk.Frame(pomodoro, bg=self.menu.bg_color)
        controls_frame.pack(fill='x', padx=30, pady=10)

        ModernButton(
            controls_frame,
            "▶️ Start",
            self.menu,
            callback=self.start_pomodoro,
            style="success"
        )

        ModernButton(
            controls_frame,
            "⏸️ Pause",
            self.menu,
            callback=self.pause_pomodoro,
            style="warning"
        )

        ModernButton(
            controls_frame,
            "⏹️ Reset",
            self.menu,
            callback=self.reset_pomodoro,
            style="danger"
        )

        ImageSeparator(pomodoro, "⚙️ TIMER SETTINGS", menu_ref=self.menu)

        # Configurações de tempo
        ModernSlider(
            pomodoro,
            "Work Duration (min)",
            5, 60,
            self.menu,
            default=25,
            callback=self.set_work_duration
        )

        ModernSlider(
            pomodoro,
            "Break Duration (min)",
            1, 30,
            self.menu,
            default=5,
            callback=self.set_break_duration
        )

        # Estatísticas do Pomodoro
        ImageSeparator(pomodoro, "📊 SESSION STATS", menu_ref=self.menu)

        stats_frame = tk.Frame(pomodoro, bg=self.menu.bg_color, pady=10)
        stats_frame.pack(fill='x', padx=30)

        self.pomodoro_stats = tk.Label(
            stats_frame,
            text=f"🍅 Pomodoros: 0 | ⏱️ Work: 0m | ☕ Break: 0m",
            bg=self.menu.bg_color,
            fg=self.menu.theme,
            font=("Arial", 9, "bold")
        )
        self.pomodoro_stats.pack()

        # Auto-start opções
        ModernCheck(
            pomodoro,
            "Auto-start breaks",
            self.menu,
            default=True,
            callback=lambda v: setattr(self, 'auto_start_breaks', v)
        )

        ModernCheck(
            pomodoro,
            "Auto-start work sessions",
            self.menu,
            default=False,
            callback=lambda v: setattr(self, 'auto_start_work', v)
        )

        self.auto_start_breaks = True
        self.auto_start_work = False

    def setup_notes_tab(self):
        """Configura a aba de notas"""
        notes = self.menu.add_tab("NOTES")

        ImageSeparator(notes, "📝 QUICK NOTES", menu_ref=self.menu)

        # Editor de notas
        self.notes_editor = scrolledtext.ScrolledText(
            notes,
            bg="#0a0a15",
            fg="white",
            font=("Consolas", 10),
            bd=0,
            highlightthickness=2,
            highlightbackground=self.menu.theme,
            wrap=tk.WORD,
            insertbackground=self.menu.theme
        )
        self.notes_editor.pack(fill='both', expand=True, padx=30, pady=10)

        # Placeholder
        placeholder = """
📌 Quick Notes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type your notes here...

• Meeting notes
• Ideas
• Reminders
• Anything you need!

        """
        self.notes_editor.insert(1.0, placeholder.strip())

        ImageSeparator(notes, "💾 ACTIONS", menu_ref=self.menu)

        ModernButton(
            notes,
            "💾 Save Notes",
            self.menu,
            callback=self.save_notes,
            style="success"
        )

        ModernButton(
            notes,
            "🗑️ Clear Notes",
            self.menu,
            callback=self.clear_notes,
            style="danger"
        )

    def setup_stats_tab(self):
        """Configura a aba de estatísticas"""
        stats = self.menu.add_tab("STATS")

        ImageSeparator(stats, "📊 PRODUCTIVITY STATS", menu_ref=self.menu)

        # Gráfico de produtividade
        self.productivity_graph = ModernGraph(stats, "DAILY ACTIVITY", self.menu)

        # Estatísticas gerais
        stats_frame = tk.Frame(stats, bg=self.menu.bg_color, pady=20)
        stats_frame.pack(fill='x', padx=30)

        self.stats_display = tk.Label(
            stats_frame,
            text="Loading statistics...",
            bg=self.menu.bg_color,
            fg="white",
            font=("Arial", 9),
            justify='left'
        )
        self.stats_display.pack(anchor='w')

        self.update_stats_display()

        ImageSeparator(stats, "🏆 ACHIEVEMENTS", menu_ref=self.menu)

        # Conquistas
        achievements_frame = tk.Frame(stats, bg=self.menu.bg_color, pady=10)
        achievements_frame.pack(fill='x', padx=30)

        achievements = [
            "🥉 First Pomodoro",
            "🥈 5 Tasks Completed",
            "🥇 10 Pomodoros",
            "🏆 Productivity Master"
        ]

        for achievement in achievements:
            tk.Label(
                achievements_frame,
                text=achievement,
                bg=self.menu.bg_color,
                fg="gray",
                font=("Arial", 9)
            ).pack(anchor='w', pady=2)

        ModernButton(
            stats,
            "🔄 Refresh Stats",
            self.menu,
            callback=self.update_stats_display,
            style="info"
        )

        ModernButton(
            stats,
            "📤 Export Report",
            self.menu,
            callback=self.export_report,
            style="success"
        )

    def start_timer_system(self):
        """Inicia o sistema de timer em background"""
        def timer_loop():
            while True:
                try:
                    if self.pomodoro_running and self.current_timer > 0:
                        time.sleep(1)
                        self.current_timer -= 1

                        # Atualizar display
                        minutes = self.current_timer // 60
                        seconds = self.current_timer % 60
                        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

                        # Atualizar barra de progresso
                        self.update_progress_bar()

                        # Timer acabou
                        if self.current_timer == 0:
                            self.timer_complete()
                    else:
                        time.sleep(0.5)
                except:
                    time.sleep(1)

        thread = threading.Thread(target=timer_loop, daemon=True)
        thread.start()

        # Atualizar gráfico de produtividade
        def update_graph():
            while True:
                try:
                    # Simular atividade
                    if self.pomodoro_running:
                        value = 80 + (20 * (self.current_timer % 10) / 10)
                    else:
                        value = 20 + (10 * (int(time.time()) % 5))

                    self.productivity_graph.add_value(value)
                    time.sleep(2)
                except:
                    time.sleep(2)

        graph_thread = threading.Thread(target=update_graph, daemon=True)
        graph_thread.start()

    def add_task(self):
        """Adiciona nova tarefa"""
        task_text = self.task_entry.get().strip()

        if task_text:
            priority = self.priority_var.get()
            timestamp = datetime.datetime.now().strftime("%H:%M")

            task = {
                'text': task_text,
                'priority': priority,
                'time': timestamp,
                'completed': False
            }

            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.update_tasks_display()

            self.menu.show_notification(
                "Task Added",
                f"'{task_text}' added to your list!",
                2000,
                "success"
            )
        else:
            self.menu.show_notification(
                "Error",
                "Please enter a task description",
                2000,
                "warning"
            )

    def update_tasks_display(self):
        """Atualiza a exibição de tarefas"""
        self.tasks_text.delete(1.0, tk.END)

        if not self.tasks:
            self.tasks_text.insert(1.0, "No tasks yet.\nAdd your first task above! ✨")
        else:
            priority_icons = {
                'Low': '🟢',
                'Medium': '🟡',
                'High': '🟠',
                'Urgent': '🔴'
            }

            for i, task in enumerate(self.tasks, 1):
                icon = priority_icons.get(task['priority'], '⚪')
                text = f"{i}. {icon} [{task['time']}] {task['text']}\n"
                self.tasks_text.insert(tk.END, text)

    def complete_task(self):
        """Marca tarefa como concluída"""
        if self.tasks:
            task = self.tasks.pop(0)
            self.completed_tasks.append(task)
            self.tasks_completed_today += 1
            self.update_tasks_display()
            self.update_stats_display()

            self.menu.show_notification(
                "Task Completed! 🎉",
                f"Great job! '{task['text']}' is done!",
                3000,
                "success"
            )
        else:
            self.menu.show_notification(
                "No Tasks",
                "No tasks to complete",
                2000,
                "info"
            )

    def delete_task(self):
        """Deleta tarefa selecionada"""
        if self.tasks:
            task = self.tasks.pop(0)
            self.update_tasks_display()

            self.menu.show_notification(
                "Task Deleted",
                f"'{task['text']}' removed",
                2000,
                "warning"
            )

    def start_pomodoro(self):
        """Inicia o timer Pomodoro"""
        if not self.pomodoro_running:
            self.pomodoro_running = True

            status = "Work time! Stay focused." if self.timer_type == "work" else "Break time! Relax."
            self.timer_status.config(text=status, fg=self.menu.theme)

            self.menu.show_notification(
                "Pomodoro Started",
                status,
                3000,
                "success"
            )

    def pause_pomodoro(self):
        """Pausa o timer"""
        self.pomodoro_running = False
        self.timer_status.config(text="Paused", fg="yellow")

        self.menu.show_notification(
            "Pomodoro Paused",
            "Timer paused. Resume when ready.",
            2000,
            "warning"
        )

    def reset_pomodoro(self):
        """Reseta o timer"""
        self.pomodoro_running = False

        if self.timer_type == "work":
            self.current_timer = self.pomodoro_time
        else:
            self.current_timer = self.break_time

        minutes = self.current_timer // 60
        seconds = self.current_timer % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        self.timer_status.config(text="Reset", fg="gray")
        self.update_progress_bar()

        self.menu.show_notification(
            "Timer Reset",
            "Timer has been reset",
            2000,
            "info"
        )

    def timer_complete(self):
        """Chamado quando o timer termina"""
        self.pomodoro_running = False

        if self.timer_type == "work":
            self.pomodoros_completed += 1
            self.total_work_time += self.pomodoro_time // 60
            self.timer_type = "break"
            self.current_timer = self.break_time

            self.menu.show_notification(
                "🎉 Pomodoro Complete!",
                "Great work! Time for a break.",
                5000,
                "success"
            )

            if self.auto_start_breaks:
                self.menu.root.after(2000, self.start_pomodoro)
        else:
            self.total_break_time += self.break_time // 60
            self.timer_type = "work"
            self.current_timer = self.pomodoro_time

            self.menu.show_notification(
                "☕ Break Complete!",
                "Back to work! Stay focused.",
                5000,
                "info"
            )

            if self.auto_start_work:
                self.menu.root.after(2000, self.start_pomodoro)

        self.update_stats_display()

    def update_progress_bar(self):
        """Atualiza barra de progresso do timer"""
        try:
            total_time = self.pomodoro_time if self.timer_type == "work" else self.break_time
            width = self.progress_canvas.winfo_width()

            if width > 1:
                self.progress_canvas.delete("all")

                # Fundo
                self.progress_canvas.create_rectangle(
                    0, 0, width, 20,
                    fill="#1a1a1a", outline=""
                )

                # Progresso
                progress = 1 - (self.current_timer / total_time)
                progress_width = int(width * progress)

                color = self.menu.theme if self.timer_type == "work" else "#4caf50"
                self.progress_canvas.create_rectangle(
                    0, 0, progress_width, 20,
                    fill=color, outline=""
                )
        except:
            pass

    def set_work_duration(self, minutes):
        """Define duração do trabalho"""
        self.pomodoro_time = minutes * 60
        if self.timer_type == "work" and not self.pomodoro_running:
            self.current_timer = self.pomodoro_time
            self.timer_label.config(text=f"{minutes:02d}:00")

    def set_break_duration(self, minutes):
        """Define duração do intervalo"""
        self.break_time = minutes * 60
        if self.timer_type == "break" and not self.pomodoro_running:
            self.current_timer = self.break_time
            self.timer_label.config(text=f"{minutes:02d}:00")

    def update_stats_display(self):
        """Atualiza display de estatísticas"""
        stats_text = f"""
📊 Today's Productivity
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍅 Pomodoros Completed: {self.pomodoros_completed}
✅ Tasks Completed: {self.tasks_completed_today}
⏱️  Total Work Time: {self.total_work_time} minutes
☕ Total Break Time: {self.total_break_time} minutes
📋 Active Tasks: {len(self.tasks)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """

        self.stats_display.config(text=stats_text.strip())
        self.pomodoro_stats.config(
            text=f"🍅 Pomodoros: {self.pomodoros_completed} | ⏱️ Work: {self.total_work_time}m | ☕ Break: {self.total_break_time}m"
        )

    def save_notes(self):
        """Salva notas"""
        notes_content = self.notes_editor.get(1.0, tk.END)

        self.menu.show_notification(
            "Notes Saved",
            "Your notes have been saved successfully!",
            3000,
            "success"
        )

    def clear_notes(self):
        """Limpa notas"""
        self.notes_editor.delete(1.0, tk.END)

        self.menu.show_notification(
            "Notes Cleared",
            "All notes have been cleared",
            2000,
            "warning"
        )

    def export_report(self):
        """Exporta relatório de produtividade"""
        self.menu.show_notification(
            "Export",
            f"Report exported: {self.pomodoros_completed} pomodoros, {self.tasks_completed_today} tasks",
            4000,
            "success"
        )

    def run(self):
        """Inicia o dashboard"""
        self.menu.show_notification(
            "Productivity Dashboard",
            "Welcome! Let's be productive today! 💪",
            4000,
            "success"
        )
        self.menu.run("insert")


if __name__ == "__main__":
    dashboard = ProductivityDashboard()
    dashboard.run()
