import os
# Silenciar mensagens do Pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import tkinter as tk
from tkinter import Frame, Canvas, messagebox
import keyboard
import colorsys
import math
import random
import threading
import time
from PIL import Image, ImageTk, ImageDraw, ImageEnhance
import pygame
import win32gui
import win32process
import psutil
import ctypes

class ProcessOverlay:
    """Overlay transparente que acompanha a janela de um processo"""
    def __init__(self, process_name, bg_color="#000000", alpha=0.3):
        """
        Args:
            process_name: Nome do processo (ex: "notepad.exe" ou "chrome.exe")
            bg_color: Cor de fundo do overlay
            alpha: Transparência (0.0 a 1.0)
        """
        self.process_name = process_name
        self.hwnd = None
        self.running = False
        self.alpha = alpha

        # Criar janela overlay
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", bg_color)
        self.root.attributes("-alpha", alpha)
        self.root.config(bg=bg_color)

        # Canvas para desenho
        self.canvas = tk.Canvas(
            self.root,
            bg=bg_color,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill='both', expand=True)

        # Desenhos customizados
        self.drawings = []

    def find_process_window(self):
        """Encontra a janela do processo pelo nome"""
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    process = psutil.Process(pid)
                    if process.name().lower() == self.process_name.lower():
                        hwnds.append(hwnd)
                except:
                    pass
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds[0] if hwnds else None

    def get_window_rect(self, hwnd):
        """Obtém posição e tamanho da janela"""
        try:
            rect = win32gui.GetWindowRect(hwnd)
            x, y = rect[0], rect[1]
            w = rect[2] - rect[0]
            h = rect[3] - rect[1]
            return x, y, w, h
        except:
            return None

    def update_position(self):
        """Atualiza posição do overlay para seguir a janela do processo"""
        if not self.running:
            return

        try:
            # Encontrar janela se ainda não foi encontrada
            if not self.hwnd:
                self.hwnd = self.find_process_window()

            if self.hwnd:
                # Verificar se janela ainda existe
                if not win32gui.IsWindow(self.hwnd):
                    self.hwnd = self.find_process_window()

                if self.hwnd:
                    rect = self.get_window_rect(self.hwnd)
                    if rect:
                        x, y, w, h = rect
                        self.root.geometry(f"{w}x{h}+{x}+{y}")
        except:
            self.hwnd = None

        # Continuar atualizando
        if self.running:
            self.root.after(16, self.update_position)  # ~60 FPS

    def draw_rectangle(self, x, y, width, height, color="red", thickness=2, fill=None):
        """Desenha um retângulo no overlay"""
        rect_id = self.canvas.create_rectangle(
            x, y, x + width, y + height,
            outline=color,
            width=thickness,
            fill=fill if fill else ""
        )
        self.drawings.append(rect_id)
        return rect_id

    def draw_line(self, x1, y1, x2, y2, color="red", thickness=2):
        """Desenha uma linha no overlay"""
        line_id = self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=thickness
        )
        self.drawings.append(line_id)
        return line_id

    def draw_circle(self, x, y, radius, color="red", thickness=2, fill=None):
        """Desenha um círculo no overlay"""
        circle_id = self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            outline=color,
            width=thickness,
            fill=fill if fill else ""
        )
        self.drawings.append(circle_id)
        return circle_id

    def draw_text(self, x, y, text, color="white", font=("Arial", 12, "bold")):
        """Desenha texto no overlay"""
        text_id = self.canvas.create_text(
            x, y,
            text=text,
            fill=color,
            font=font
        )
        self.drawings.append(text_id)
        return text_id

    def draw_crosshair(self, x, y, size=20, color="lime", thickness=2):
        """Desenha uma mira (crosshair) no overlay"""
        # Linha horizontal
        self.draw_line(x - size, y, x + size, y, color, thickness)
        # Linha vertical
        self.draw_line(x, y - size, x, y + size, color, thickness)

    def clear_drawings(self):
        """Limpa todos os desenhos"""
        for drawing_id in self.drawings:
            try:
                self.canvas.delete(drawing_id)
            except:
                pass
        self.drawings.clear()

    def delete_drawing(self, drawing_id):
        """Remove um desenho específico"""
        try:
            self.canvas.delete(drawing_id)
            if drawing_id in self.drawings:
                self.drawings.remove(drawing_id)
        except:
            pass

    def set_alpha(self, alpha):
        """Define a transparência do overlay (0.0 a 1.0)"""
        self.alpha = max(0.0, min(1.0, alpha))
        self.root.attributes("-alpha", self.alpha)

    def start(self):
        """Inicia o overlay"""
        self.running = True

        # Procurar janela do processo
        self.hwnd = self.find_process_window()

        if not self.hwnd:
            print(f"Processo '{self.process_name}' não encontrado!")
            return False

        # Iniciar atualização de posição
        self.update_position()

        return True

    def stop(self):
        """Para o overlay"""
        self.running = False
        try:
            self.root.destroy()
        except:
            pass

    def run(self):
        """Inicia o loop principal do overlay"""
        if self.start():
            self.root.mainloop()


class NotificationManager:
    """Gerenciador de notificações estilo Roblox - CORRIGIDO"""
    def __init__(self):
        self.notifications = []
        self.notification_windows = []
        self.lock = threading.Lock()

    def show(self, title, message, duration=3000, notification_type="info"):
        """
        Mostra uma notificação no canto inferior direito
        tipos: 'info', 'success', 'warning', 'error'
        """
        # Cores baseadas no tipo
        colors = {
            'info': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'error': '#e74c3c'
        }

        color = colors.get(notification_type, '#3498db')

        # Criar janela de notificação
        notif = tk.Toplevel()
        notif.overrideredirect(True)
        notif.attributes("-topmost", True)
        notif.attributes("-alpha", 0.0)  # Começa invisível

        # Configurar posição (canto inferior direito)
        screen_width = notif.winfo_screenwidth()
        screen_height = notif.winfo_screenheight()

        width = 320
        height = 90

        # Calcular posição Y baseado em quantas notificações já existem
        with self.lock:
            offset = len(self.notification_windows) * (height + 10)

        x = screen_width - width - 20
        y = screen_height - height - 60 - offset

        notif.geometry(f"{width}x{height}+{x}+{y}")

        # Frame principal com borda
        main_frame = tk.Frame(notif, bg=color, bd=0)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)

        inner_frame = tk.Frame(main_frame, bg="#1a1a1a", bd=0)
        inner_frame.pack(fill='both', expand=True)

        # Header com título
        header = tk.Frame(inner_frame, bg=color, height=30, bd=0)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)

        tk.Label(header, text=title.upper(), bg=color, fg="white",
                font=("Arial", 9, "bold")).pack(side='left', padx=10, pady=5)

        # Botão fechar
        close_btn = tk.Label(header, text="✕", bg=color, fg="white",
                            font=("Arial", 10), cursor="hand2")
        close_btn.pack(side='right', padx=10)
        close_btn.bind("<Button-1>", lambda e: self._close_notification(notif))

        # Mensagem
        msg_frame = tk.Frame(inner_frame, bg="#1a1a1a", bd=0)
        msg_frame.pack(fill='both', expand=True, padx=10, pady=5)

        tk.Label(msg_frame, text=message, bg="#1a1a1a", fg="white",
                font=("Arial", 8), wraplength=280, justify='left').pack(anchor='w')

        # Barra de progresso
        progress_canvas = tk.Canvas(inner_frame, height=3, bg="#1a1a1a",
                                   highlightthickness=0, bd=0)
        progress_canvas.pack(fill='x', side='bottom')

        progress_bar = progress_canvas.create_rectangle(0, 0, width, 3,
                                                        fill=color, outline="")

        with self.lock:
            self.notification_windows.append(notif)

        # Animação de entrada (slide + fade)
        self._animate_in(notif, x, y, width)

        # Iniciar timer de progresso - CORRIGIDO
        self._start_progress_fixed(notif, progress_canvas, progress_bar,
                                   duration, width, color)

        return notif

    def _start_progress_fixed(self, window, canvas, bar, duration, width, color):
        """Anima a barra de progresso - VERSÃO CORRIGIDA"""
        start_time = time.time()
        closed = {'value': False}  # Usar dicionário para evitar problemas de escopo
        after_ids = []  # Rastrear IDs de callbacks

        def update():
            # Verificar se foi fechada manualmente
            if closed['value']:
                return

            try:
                # Verificar se janela ainda existe
                if not window.winfo_exists():
                    closed['value'] = True
                    return
            except:
                closed['value'] = True
                return

            # Calcular progresso
            elapsed = (time.time() - start_time) * 1000
            progress = min(elapsed / duration, 1.0)

            try:
                # Atualizar barra
                remaining_width = width * (1 - progress)
                canvas.coords(bar, 0, 0, remaining_width, 3)
            except:
                closed['value'] = True
                return

            # Continuar ou fechar
            if progress < 1.0:
                # Agendar próxima atualização
                after_id = window.after(16, update)
                after_ids.append(after_id)
            else:
                # Tempo acabou, fechar
                closed['value'] = True
                self._close_notification(window)

        # Função para cancelar ao fechar manualmente
        def cancel_updates():
            closed['value'] = True
            for after_id in after_ids:
                try:
                    window.after_cancel(after_id)
                except:
                    pass

        # Associar cancelamento ao botão X
        window.cancel_progress = cancel_updates

        # Iniciar loop
        update()

    def _animate_in(self, window, target_x, target_y, width):
        """Animação de entrada (slide da direita + fade)"""
        start_x = target_x + width
        steps = 15
        delay = 15

        def animate(step=0):
            try:
                if not window.winfo_exists():
                    return

                if step <= steps:
                    # Calcular posições e alpha
                    progress = step / steps
                    current_x = start_x - (start_x - target_x) * self._ease_out_cubic(progress)
                    alpha = progress * 0.95

                    window.geometry(f"+{int(current_x)}+{target_y}")
                    window.attributes("-alpha", alpha)

                    window.after(delay, lambda: animate(step + 1))
            except:
                pass

        animate()

    def _animate_out(self, window, callback=None):
        """Animação de saída (slide para direita + fade)"""
        try:
            if not window.winfo_exists():
                if callback:
                    callback()
                return

            current_x = window.winfo_x()
            target_x = current_x + 350
            current_y = window.winfo_y()
            steps = 15
            delay = 15

            def animate(step=0):
                try:
                    if not window.winfo_exists():
                        if callback:
                            callback()
                        return

                    if step <= steps:
                        progress = step / steps
                        new_x = current_x + (target_x - current_x) * self._ease_in_cubic(progress)
                        alpha = 1.0 - progress

                        window.geometry(f"+{int(new_x)}+{current_y}")
                        window.attributes("-alpha", alpha * 0.95)

                        window.after(delay, lambda: animate(step + 1))
                    else:
                        if callback:
                            callback()
                except:
                    if callback:
                        callback()

            animate()
        except:
            if callback:
                callback()

    def _ease_out_cubic(self, t):
        """Easing function para animação suave"""
        return 1 - pow(1 - t, 3)

    def _ease_in_cubic(self, t):
        """Easing function para animação suave"""
        return t * t * t

    def _close_notification(self, window):
        """Fecha a notificação com animação"""
        try:
            if not window.winfo_exists():
                return
        except:
            return

        # Cancelar progresso se existir
        if hasattr(window, 'cancel_progress'):
            try:
                window.cancel_progress()
            except:
                pass

        with self.lock:
            if window in self.notification_windows:
                self.notification_windows.remove(window)

        def destroy():
            try:
                if window.winfo_exists():
                    window.destroy()
            except:
                pass

            # Reposicionar após pequeno delay
            if self.notification_windows:
                try:
                    # Usar primeira notificação válida para agendar reposicionamento
                    valid_windows = [w for w in self.notification_windows if self._is_window_valid(w)]
                    if valid_windows:
                        valid_windows[0].after(50, self._reposition_notifications)
                except:
                    pass

        self._animate_out(window, destroy)

    def _is_window_valid(self, window):
        """Verifica se janela ainda é válida"""
        try:
            return window.winfo_exists()
        except:
            return False

    def _reposition_notifications(self):
        """Reposiciona notificações após fechamento"""
        try:
            with self.lock:
                # Filtrar apenas janelas válidas
                self.notification_windows = [w for w in self.notification_windows if self._is_window_valid(w)]

                if not self.notification_windows:
                    return

                # Obter dimensões da tela
                first_notif = self.notification_windows[0]
                screen_height = first_notif.winfo_screenheight()
                screen_width = first_notif.winfo_screenwidth()

                for i, notif in enumerate(self.notification_windows):
                    try:
                        if self._is_window_valid(notif):
                            height = 90
                            offset = i * (height + 10)
                            x = screen_width - 320 - 20
                            y = screen_height - height - 60 - offset

                            # Animação suave para reposicionamento
                            self._smooth_move(notif, y)
                    except:
                        continue
        except:
            pass

    def _smooth_move(self, window, target_y):
        """Move suavemente a janela para nova posição Y"""
        try:
            if not self._is_window_valid(window):
                return

            current_y = window.winfo_y()
            diff = target_y - current_y

            if abs(diff) < 2:
                window.geometry(f"+{window.winfo_x()}+{target_y}")
                return

            new_y = current_y + diff * 0.3
            window.geometry(f"+{window.winfo_x()}+{int(new_y)}")
            window.after(16, lambda: self._smooth_move(window, target_y))
        except:
            pass


class MessageBox:
    """MessageBox personalizado estilo CLIV (sem bordas do Windows)"""
    @staticmethod
    def show(title, message, msg_type="info", theme_color="#8e44ad"):
        """
        Mostra um messagebox personalizado
        tipos: 'info', 'success', 'warning', 'error', 'question'
        """
        box = tk.Toplevel()
        box.overrideredirect(True)  # Remove bordas do Windows
        box.geometry("420x220")
        box.configure(bg="#05050a")
        box.attributes("-topmost", True)

        # Centralizar na tela
        box.update_idletasks()
        x = (box.winfo_screenwidth() // 2) - (420 // 2)
        y = (box.winfo_screenheight() // 2) - (220 // 2)
        box.geometry(f"420x220+{x}+{y}")

        # Cores baseadas no tipo
        colors = {
            'info': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'question': '#9b59b6'
        }

        icons = {
            'info': 'ℹ',
            'success': '✓',
            'warning': '⚠',
            'error': '✕',
            'question': '?'
        }

        color = colors.get(msg_type, theme_color)
        icon = icons.get(msg_type, 'ℹ')

        # Header (igual ao menu principal)
        header = tk.Frame(box, bg=color, height=35, bd=0)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)

        # Ícone + Título
        title_frame = tk.Frame(header, bg=color)
        title_frame.pack(side='left', fill='y', padx=10)

        tk.Label(title_frame, text=icon, bg=color, fg="white",
                font=("Arial", 14, "bold")).pack(side='left', padx=(0, 8))
        tk.Label(title_frame, text=title.upper(), bg=color, fg="white",
                font=("Impact", 10)).pack(side='left')

        # Botão fechar (X)
        close_btn = tk.Button(header, text="✕", command=box.destroy,
                             bg=color, fg="white", bd=0, width=5,
                             activebackground="#ff4444", cursor="hand2",
                             font=("Arial", 10))
        close_btn.pack(side='right', fill='y')

        # Permitir arrastar pela header
        def start_move(event):
            box.x = event.x
            box.y = event.y

        def on_move(event):
            deltax = event.x - box.x
            deltay = event.y - box.y
            new_x = box.winfo_x() + deltax
            new_y = box.winfo_y() + deltay
            box.geometry(f"+{new_x}+{new_y}")

        header.bind("<Button-1>", start_move)
        header.bind("<B1-Motion>", on_move)
        title_frame.bind("<Button-1>", start_move)
        title_frame.bind("<B1-Motion>", on_move)

        # Corpo da mensagem
        body = tk.Frame(box, bg="#05050a", bd=0)
        body.pack(fill='both', expand=True, padx=25, pady=20)

        # Mensagem com scroll se necessário
        msg_label = tk.Label(body, text=message, bg="#05050a", fg="white",
                            font=("Arial", 9), wraplength=370, justify='left')
        msg_label.pack(expand=True)

        # Botão OK
        btn_frame = tk.Frame(box, bg="#05050a", bd=0)
        btn_frame.pack(fill='x', padx=25, pady=(0, 20))

        ok_btn = tk.Button(btn_frame, text="OK", bg=color, fg="white",
                          font=("Arial", 9, "bold"), bd=0, width=18,
                          command=box.destroy, cursor="hand2",
                          activebackground=color, activeforeground="white",
                          relief='flat')
        ok_btn.pack(side='right', ipady=8)

        # Efeito hover
        def on_enter(e):
            ok_btn.config(relief='raised')
        def on_leave(e):
            ok_btn.config(relief='flat')

        ok_btn.bind("<Enter>", on_enter)
        ok_btn.bind("<Leave>", on_leave)

        # Animação de entrada (fade in)
        box.attributes("-alpha", 0.0)

        def fade_in(alpha=0.0):
            if alpha < 0.95:
                alpha += 0.1
                box.attributes("-alpha", alpha)
                box.after(20, lambda: fade_in(alpha))

        box.after(10, fade_in)

        box.grab_set()
        box.focus_force()
        box.wait_window()


class ClivMenu:
    def __init__(self, title="CLIV1 EXTREME", theme_color="#8e44ad", bg_img_path=None,
                 part_color="white", part_count=40, part_speed=(0.2, 0.8),
                 enable_tray_icon=False, tray_icon_path=None):
        self.root = tk.Tk()
        self.theme = theme_color
        self.bg_color = "#05050a"
        self.data = {}
        self.abas = {}
        self.botoes_abas = {}
        self.aba_atual = None
        self.aberto = True
        self.bg_img_path = bg_img_path
        self.title = title

        # Configuração de Partículas
        self.p_color = part_color
        self.p_count = part_count
        self.p_speed_range = part_speed

        # Sistema de Notificações
        self.notif_manager = NotificationManager()

        # System Tray Icon
        self.enable_tray = enable_tray_icon
        self.tray_icon_path = tray_icon_path
        self.tray_icon = None
        self.tray_thread = None

        # Inicializar Áudio
        try:
            pygame.mixer.init()
        except:
            pass

        self._setup_main_ui(title)
        self._init_particles()

        # Inicializar tray icon se habilitado
        if self.enable_tray:
            self._init_tray_icon()

    def _setup_main_ui(self, title):
        self.root.geometry("450x720")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg=self.bg_color)

        # Canvas de Fundo (Camada 0)
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0, bg=self.bg_color, bd=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        if self.bg_img_path and os.path.exists(self.bg_img_path):
            try:
                img = Image.open(self.bg_img_path).resize((450, 720), Image.Resampling.LANCZOS)
                img = ImageEnhance.Brightness(img).enhance(0.15)
                self.bg_photo = ImageTk.PhotoImage(img)
                self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            except Exception as e:
                print(f"Erro ao carregar imagem de fundo: {e}")

        # Header
        self.header = tk.Frame(self.root, bg=self.theme, height=35, bd=0)
        self.header.pack(fill='x', side='top')
        self.header.pack_propagate(False)

        tk.Label(self.header, text=title, bg=self.theme, fg="white",
                font=("Impact", 11)).pack(side='left', padx=15)

        # Botão minimizar
        min_btn = tk.Button(self.header, text="−", command=self.toggle_visibility,
                           bg=self.theme, fg="white", bd=0, width=5,
                           activebackground="#555", cursor="hand2")
        min_btn.pack(side='right', fill='y')

        # Botão fechar
        close_btn = tk.Button(self.header, text="✕", command=self._on_close,
                             bg=self.theme, fg="white", bd=0, width=5,
                             activebackground="#ff4444", cursor="hand2")
        close_btn.pack(side='right', fill='y')

        self.header.bind("<Button-1>", self._start_move)
        self.header.bind("<B1-Motion>", self._on_move)

        # Barra de Abas
        self.tab_bar = tk.Frame(self.root, bg="#000", height=35, bd=0)
        self.tab_bar.pack(fill='x', side='top')
        self.tab_bar.pack_propagate(False)

        # Container principal para abas
        self.container_principal = tk.Frame(self.root, bg=self.bg_color, bd=0)
        self.container_principal.place(x=0, y=70, width=450, height=650)

    def _init_particles(self):
        """Inicializa sistema de partículas com melhorias"""
        self.particles = []
        for _ in range(self.p_count):
            self.particles.append({
                'id': self.bg_canvas.create_oval(0, 0, 2, 2, fill=self.p_color, outline=""),
                'x': random.randint(0, 450),
                'y': random.randint(0, 720),
                'speed': random.uniform(self.p_speed_range[0], self.p_speed_range[1]),
                'opacity': random.uniform(0.3, 1.0)
            })
        self._update_particles()

    def _init_tray_icon(self):
        """Inicializa o ícone na system tray (Windows)"""
        try:
            from pystray import Icon, Menu, MenuItem
            from PIL import Image, ImageDraw

            # Criar ícone se não foi fornecido
            if self.tray_icon_path and os.path.exists(self.tray_icon_path):
                icon_image = Image.open(self.tray_icon_path)
            else:
                # Criar ícone padrão (círculo colorido)
                icon_image = self._create_default_icon()

            # Criar menu do tray
            menu = Menu(
                MenuItem('Mostrar/Ocultar', self.toggle_visibility, default=True),
                MenuItem('Notificação de Teste', self._tray_test_notification),
                Menu.SEPARATOR,
                MenuItem('Fechar', self._tray_quit)
            )

            # Criar ícone
            self.tray_icon = Icon(
                name=self.title,
                icon=icon_image,
                title=self.title,
                menu=menu
            )

            # Rodar em thread separada
            self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            self.tray_thread.start()

            # Notificação de sucesso
            self.root.after(800, lambda: self.show_notification(
                "System Tray",
                "Ícone adicionado à bandeja do sistema!",
                3000,
                "success"
            ))

        except ImportError:
            self.show_notification(
                "Erro",
                "pystray não instalado! Execute: pip install pystray",
                5000,
                "error"
            )
        except Exception as e:
            print(f"Erro ao criar tray icon: {e}")

    def _create_default_icon(self):
        """Cria um ícone padrão caso não seja fornecido"""
        # Criar imagem 64x64
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Desenhar círculo com a cor do tema
        # Converter hex para RGB
        hex_color = self.theme.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # Círculo externo
        draw.ellipse([4, 4, 60, 60], fill=rgb, outline=(255, 255, 255))

        # Círculo interno (destaque)
        lighter = tuple(min(c + 50, 255) for c in rgb)
        draw.ellipse([16, 16, 48, 48], fill=lighter)

        return image

    def _tray_test_notification(self):
        """Mostra notificação de teste via tray icon"""
        self.show_notification(
            "Tray Icon",
            "Clique com botão direito no ícone para mais opções!",
            3000,
            "info"
        )

    def _tray_quit(self):
        """Fecha o programa via tray icon"""
        if self.tray_icon:
            self.tray_icon.stop()
        self._on_close()

    def _update_particles(self):
        """Atualiza partículas com efeito de fade"""
        if not self.aberto or not self.root.winfo_exists():
            return

        try:
            for p in self.particles:
                p['y'] -= p['speed']
                if p['y'] < 0:
                    p['y'] = 720
                    p['x'] = random.randint(0, 450)

                # Atualizar posição
                self.bg_canvas.coords(p['id'], p['x'], p['y'], p['x']+2, p['y']+2)

            self.root.after(30, self._update_particles)
        except:
            pass

    def add_tab(self, name):
        """Adiciona uma nova aba ao menu"""
        # Frame com scrollbar CUSTOMIZADO
        frame_container = tk.Frame(self.container_principal, bg=self.bg_color, bd=0)

        canvas = tk.Canvas(frame_container, bg=self.bg_color, highlightthickness=0, bd=0)

        # SCROLLBAR CUSTOMIZADO - Estilo moderno
        scrollbar_frame = tk.Frame(frame_container, bg=self.bg_color, width=8, bd=0)
        scrollbar_canvas = tk.Canvas(scrollbar_frame, bg="#0a0a15", width=8,
                                     highlightthickness=0, bd=0)
        scrollbar_canvas.pack(fill='both', expand=True)

        # Variáveis para o scrollbar custom
        scroll_data = {
            'dragging': False,
            'start_y': 0,
            'thumb': None,
            'thumb_y': 0,
            'thumb_height': 100
        }

        def update_scrollbar(*args):
            """Atualiza a posição e tamanho do thumb do scrollbar"""
            try:
                # Obter informações de scroll
                first, last = canvas.yview()
                canvas_height = scrollbar_canvas.winfo_height()

                if canvas_height < 10:
                    return

                # Calcular tamanho e posição do thumb
                visible_ratio = last - first
                thumb_height = max(30, canvas_height * visible_ratio)
                thumb_y = first * canvas_height

                # Limpar e desenhar novo thumb
                scrollbar_canvas.delete("all")

                # Track (fundo)
                scrollbar_canvas.create_rectangle(
                    1, 0, 7, canvas_height,
                    fill="#0a0a15", outline=""
                )

                # Thumb (indicador)
                scroll_data['thumb'] = scrollbar_canvas.create_rectangle(
                    1, thumb_y, 7, thumb_y + thumb_height,
                    fill=self.theme, outline="", tags="thumb"
                )

                scroll_data['thumb_height'] = thumb_height
                scroll_data['thumb_y'] = thumb_y

            except:
                pass

        def on_scroll_click(event):
            """Clique no scrollbar"""
            scroll_data['dragging'] = True
            scroll_data['start_y'] = event.y

        def on_scroll_drag(event):
            """Arrastar scrollbar"""
            if scroll_data['dragging']:
                canvas_height = scrollbar_canvas.winfo_height()
                if canvas_height < 10:
                    return

                # Calcular nova posição
                delta = event.y - scroll_data['start_y']
                new_y = scroll_data['thumb_y'] + delta

                # Limites
                max_y = canvas_height - scroll_data['thumb_height']
                new_y = max(0, min(new_y, max_y))

                # Converter para fração do canvas
                fraction = new_y / canvas_height

                # Scroll do canvas
                canvas.yview_moveto(fraction)

                scroll_data['start_y'] = event.y

        def on_scroll_release(event):
            """Soltar scrollbar"""
            scroll_data['dragging'] = False

        # Bindings do scrollbar personalizado
        scrollbar_canvas.bind("<Button-1>", on_scroll_click)
        scrollbar_canvas.bind("<B1-Motion>", on_scroll_drag)
        scrollbar_canvas.bind("<ButtonRelease-1>", on_scroll_release)

        # Conectar canvas com scrollbar
        canvas.configure(yscrollcommand=lambda f, l: (update_scrollbar(f, l), None)[-1])

        scrollable_frame = tk.Frame(canvas, bg=self.bg_color, bd=0)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: (canvas.configure(scrollregion=canvas.bbox("all")), update_scrollbar())
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind mousewheel MELHORADO
        def _on_mousewheel(event):
            try:
                # Scroll mais suave
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                update_scrollbar()
            except:
                pass

        # Bind apenas quando mouse está sobre o canvas
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        scrollbar_frame.pack(side="right", fill="y", padx=(2, 0))
        canvas.pack(side="left", fill="both", expand=True)

        # Atualizar scrollbar após um delay
        frame_container.after(100, update_scrollbar)

        self.abas[name] = {
            'container': frame_container,
            'frame': scrollable_frame,
            'canvas': canvas,
            'scrollbar_canvas': scrollbar_canvas,
            'update_scroll': update_scrollbar
        }

        # Botão da aba
        btn = tk.Button(self.tab_bar, text=name.upper(), bg="#000", fg="gray",
                        activeforeground=self.theme, font=("Arial", 7, "bold"),
                        bd=0, command=lambda n=name: self.show_tab(n),
                        activebackground="#111", cursor="hand2", relief='flat')
        btn.pack(side='left', expand=True, fill='both')
        self.botoes_abas[name] = btn

        if not self.aba_atual:
            self.show_tab(name)

        return scrollable_frame

    def show_tab(self, name):
        """Mostra a aba selecionada"""
        # Esconder todas as abas
        for n, tab_data in self.abas.items():
            tab_data['container'].pack_forget()
            self.botoes_abas[n].config(fg="gray", relief='flat')

        # Mostrar aba selecionada
        self.abas[name]['container'].pack(fill='both', expand=True)
        self.botoes_abas[name].config(fg=self.theme, relief='sunken')
        self.aba_atual = name

    def set_alpha(self, val):
        """Define transparência da janela"""
        self.root.attributes("-alpha", max(0.2, min(1.0, float(val) / 100)))

    def _start_move(self, event):
        """Inicia movimentação da janela"""
        self.root.x = event.x
        self.root.y = event.y

    def _on_move(self, event):
        """Move a janela"""
        dx = event.x - self.root.x
        dy = event.y - self.root.y
        new_x = self.root.winfo_x() + dx
        new_y = self.root.winfo_y() + dy
        self.root.geometry(f"+{new_x}+{new_y}")

    def _on_close(self):
        """Fecha o menu com limpeza completa"""
        try:
            # Parar tray icon se estiver ativo
            if self.tray_icon:
                try:
                    self.tray_icon.stop()
                except:
                    pass

            # Parar todas as notificações
            for notif in list(self.notif_manager.notification_windows):
                try:
                    if notif.winfo_exists():
                        # Cancelar progresso
                        if hasattr(notif, 'cancel_progress'):
                            notif.cancel_progress()
                        notif.destroy()
                except:
                    pass

            # Limpar lista
            self.notif_manager.notification_windows.clear()

            # Parar áudio se estiver tocando
            try:
                pygame.mixer.music.stop()
            except:
                pass

            # Destruir janela principal
            self.root.quit()
            self.root.destroy()
        except:
            pass

    def show_notification(self, title, message, duration=3000, notif_type="info"):
        """Mostra notificação no canto da tela"""
        self.notif_manager.show(title, message, duration, notif_type)

    def show_message(self, title, message, msg_type="info"):
        """Mostra messagebox personalizado"""
        MessageBox.show(title, message, msg_type, self.theme)

    def run(self, hotkey="insert"):
        """Inicia o loop principal"""
        try:
            keyboard.add_hotkey(hotkey, self.toggle_visibility)
        except Exception as e:
            print(f"Erro ao registrar hotkey: {e}")

        # Mostrar notificação de boas-vindas
        self.root.after(500, lambda: self.show_notification(
            "Menu Iniciado",
            "Pressione INSERT para mostrar/ocultar",
            3000,
            "success"
        ))

        self.root.mainloop()

    def toggle_visibility(self):
        """Alterna visibilidade do menu"""
        try:
            if self.aberto:
                self.root.withdraw()
                self.aberto = False
            else:
                self.root.deiconify()
                self.aberto = True
                self._update_particles()
        except:
            pass


# --- COMPONENTES MELHORADOS ---

class AudioPlayer:
    def __init__(self, container, menu_ref, audio_path="music.mp3", autoplay=False, loop=True):
        self.menu = menu_ref
        self.shell = tk.Frame(container, bg=menu_ref.bg_color, pady=10, bd=0)
        self.shell.pack(fill='x', padx=30, pady=10)

        self.audio_path = audio_path
        self.playing = False
        self.loop = loop
        self.volume = 0.5  # Volume padrão 50%

        # Header do player
        header_frame = tk.Frame(self.shell, bg=menu_ref.bg_color)
        header_frame.pack(fill='x', pady=(0, 10))

        tk.Label(header_frame, text="🎵 AUDIO PLAYER", fg=menu_ref.theme,
                bg=menu_ref.bg_color, font=("Impact", 9)).pack(side='left')

        # Status label
        self.status_label = tk.Label(header_frame, text="●", fg="red",
                                     bg=menu_ref.bg_color, font=("Arial", 8))
        self.status_label.pack(side='right', padx=5)

        # Botões de controle
        controls_frame = tk.Frame(self.shell, bg=menu_ref.bg_color)
        controls_frame.pack(fill='x')

        # Play/Pause
        self.play_btn = tk.Button(controls_frame, text="▶", bg=menu_ref.theme,
                                  fg="white", font=("Arial", 12, "bold"), bd=0,
                                  command=self.toggle_play, cursor="hand2", width=4,
                                  activebackground=menu_ref.theme, relief='flat')
        self.play_btn.pack(side='left', padx=2, ipady=5)

        # Stop
        self.stop_btn = tk.Button(controls_frame, text="⏹", bg="#555",
                                  fg="white", font=("Arial", 12, "bold"), bd=0,
                                  command=self.stop_music, cursor="hand2", width=4,
                                  activebackground="#444", relief='flat')
        self.stop_btn.pack(side='left', padx=2, ipady=5)

        # Loop toggle
        self.loop_btn = tk.Button(controls_frame, text="🔁",
                                  bg=menu_ref.theme if loop else "#555",
                                  fg="white", font=("Arial", 10, "bold"), bd=0,
                                  command=self.toggle_loop, cursor="hand2", width=4,
                                  activebackground=menu_ref.theme, relief='flat')
        self.loop_btn.pack(side='left', padx=2, ipady=5)

        # Volume slider
        vol_frame = tk.Frame(self.shell, bg=menu_ref.bg_color)
        vol_frame.pack(fill='x', pady=(10, 0))

        tk.Label(vol_frame, text="🔊", bg=menu_ref.bg_color, fg="white",
                font=("Arial", 10)).pack(side='left', padx=(0, 5))

        self.vol_canvas = tk.Canvas(vol_frame, height=8, bg=menu_ref.bg_color,
                                    highlightthickness=0, bd=0)
        self.vol_canvas.pack(side='left', fill='x', expand=True)

        self.vol_label = tk.Label(vol_frame, text="50%", bg=menu_ref.bg_color,
                                 fg=menu_ref.theme, font=("Arial", 8, "bold"),
                                 width=4)
        self.vol_label.pack(side='right', padx=(5, 0))

        self.vol_canvas.bind("<Button-1>", self.set_volume)
        self.vol_canvas.bind("<B1-Motion>", self.set_volume)

        # Atualizar volume visual
        self.shell.after(100, self.update_volume_bar)

        # Autoplay
        if autoplay and os.path.exists(audio_path):
            self.shell.after(500, self.play_music)

    def update_volume_bar(self):
        """Atualiza a barra de volume visual"""
        try:
            width = self.vol_canvas.winfo_width()
            if width < 10:
                self.shell.after(50, self.update_volume_bar)
                return

            self.vol_canvas.delete("all")

            # Barra de fundo
            self.vol_canvas.create_rectangle(0, 2, width, 6, fill="#1a1a1a", outline="")

            # Barra de volume
            vol_width = int(width * self.volume)
            self.vol_canvas.create_rectangle(0, 2, vol_width, 6,
                                            fill=self.menu.theme, outline="")
        except:
            pass

    def set_volume(self, event):
        """Define o volume baseado no clique"""
        try:
            width = self.vol_canvas.winfo_width()
            x = max(0, min(event.x, width))
            self.volume = x / width

            pygame.mixer.music.set_volume(self.volume)
            self.vol_label.config(text=f"{int(self.volume * 100)}%")
            self.update_volume_bar()
        except:
            pass

    def toggle_play(self):
        """Alterna entre play e pause"""
        if self.playing:
            self.pause_music()
        else:
            self.play_music()

    def play_music(self):
        """Inicia a música"""
        try:
            if not self.playing:
                if os.path.exists(self.audio_path):
                    pygame.mixer.music.load(self.audio_path)
                    pygame.mixer.music.set_volume(self.volume)
                    pygame.mixer.music.play(-1 if self.loop else 0)

                    self.playing = True
                    self.play_btn.config(text="⏸")
                    self.status_label.config(fg="lime")

                    self.menu.show_notification(
                        "Audio",
                        f"Reproduzindo: {os.path.basename(self.audio_path)}",
                        2000,
                        "success"
                    )
                else:
                    self.menu.show_notification(
                        "Erro",
                        f"Arquivo não encontrado: {self.audio_path}",
                        3000,
                        "error"
                    )
            else:
                # Se já estava tocando, resume
                pygame.mixer.music.unpause()
                self.playing = True
                self.play_btn.config(text="⏸")
                self.status_label.config(fg="lime")
        except Exception as e:
            self.menu.show_notification(
                "Erro",
                f"Erro ao reproduzir: {str(e)}",
                3000,
                "error"
            )

    def pause_music(self):
        """Pausa a música"""
        try:
            if self.playing:
                pygame.mixer.music.pause()
                self.playing = False
                self.play_btn.config(text="▶")
                self.status_label.config(fg="yellow")
        except:
            pass

    def stop_music(self):
        """Para a música completamente"""
        try:
            pygame.mixer.music.stop()
            self.playing = False
            self.play_btn.config(text="▶")
            self.status_label.config(fg="red")

            self.menu.show_notification(
                "Audio",
                "Reprodução parada",
                2000,
                "info"
            )
        except:
            pass

    def toggle_loop(self):
        """Alterna modo de repetição"""
        self.loop = not self.loop

        if self.loop:
            self.loop_btn.config(bg=self.menu.theme)
            self.menu.show_notification("Loop", "Repetição ativada", 2000, "info")
        else:
            self.loop_btn.config(bg="#555")
            self.menu.show_notification("Loop", "Repetição desativada", 2000, "info")

        # Se estiver tocando, reinicia com nova configuração
        if self.playing:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.play(-1 if self.loop else 0)
            except:
                pass

    def set_audio_file(self, path):
        """Define um novo arquivo de áudio"""
        was_playing = self.playing

        if self.playing:
            self.stop_music()

        self.audio_path = path

        if was_playing and os.path.exists(path):
            self.play_music()

    def get_status(self):
        """Retorna status atual"""
        return {
            'playing': self.playing,
            'loop': self.loop,
            'volume': self.volume,
            'file': self.audio_path
        }


class ImageSeparator:
    def __init__(self, container, text, icon_path=None, menu_ref=None):
        self.shell = tk.Frame(container, bg=menu_ref.bg_color if menu_ref else "",
                             pady=10, bd=0, highlightthickness=0)
        self.shell.pack(fill='x', padx=20)

        if icon_path and os.path.exists(icon_path):
            try:
                img = Image.open(icon_path).resize((16, 16), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                tk.Label(self.shell, image=self.photo,
                        bg=menu_ref.bg_color if menu_ref else "").pack(side='left', padx=5)
            except:
                pass

        theme = menu_ref.theme if menu_ref else "#8e44ad"
        bg = menu_ref.bg_color if menu_ref else ""

        tk.Label(self.shell, text=text.upper(), fg=theme, bg=bg,
                font=("Impact", 10)).pack(side='left')
        tk.Frame(self.shell, bg=theme, height=2, bd=0).pack(fill='x', side='bottom', pady=2)


class ModernGraph:
    def __init__(self, container, label, menu_ref):
        self.menu = menu_ref
        self.shell = tk.Frame(container, bg=menu_ref.bg_color, pady=10, bd=0)
        self.shell.pack(fill='x', padx=30)
        self.values = [0] * 50

        tk.Label(self.shell, text=label, fg=menu_ref.theme, bg=menu_ref.bg_color,
                font=("Arial", 7, "bold")).pack(anchor="w")

        self.canvas = tk.Canvas(self.shell, width=350, height=60, bg="#0a0a15",
                               highlightthickness=1, highlightbackground="#222", bd=0)
        self.canvas.pack()
        self.update_graph()

    def add_value(self, val):
        """Adiciona um valor ao gráfico"""
        self.values.pop(0)
        self.values.append(val)
        self.update_graph()

    def update_graph(self):
        """Atualiza o gráfico"""
        self.canvas.delete("all")

        # Grid de fundo
        for i in range(0, 61, 20):
            self.canvas.create_line(0, i, 350, i, fill="#1a1a2e", dash=(2, 4))

        # Desenhar linha do gráfico
        points = []
        for i, v in enumerate(self.values):
            x = i * 7
            y = 60 - min(v, 120) * 0.45
            points.append((x, y))

        if len(points) > 1:
            # Gradiente de preenchimento
            for i in range(len(points)-1):
                x1, y1 = points[i]
                x2, y2 = points[i+1]
                # Linha principal
                self.canvas.create_line(x1, y1, x2, y2, fill=self.menu.theme,
                                       width=2, tags="plot", smooth=True)
                # Área preenchida
                self.canvas.create_polygon(x1, y1, x2, y2, x2, 60, x1, 60,
                                          fill=self.menu.theme, outline="",
                                          stipple="gray50", tags="fill")

            # Linha brilhante no topo
            self.canvas.tag_raise("plot")


class DynamicColorPicker:
    def __init__(self, container, var_name, menu_ref):
        self.menu = menu_ref
        self.var_name = var_name
        self.h, self.s, self.v = 0.0, 1.0, 1.0

        self.shell = tk.Frame(container, bg=menu_ref.bg_color, pady=10, bd=0)
        self.shell.pack(fill='x', padx=30)

        # Header
        head = tk.Frame(self.shell, bg=menu_ref.bg_color)
        head.pack(fill='x', pady=5)

        tk.Label(head, text=var_name.upper(), fg="white", bg=menu_ref.bg_color,
                font=("Arial", 8, "bold")).pack(side='left')

        self.preview = tk.Canvas(head, width=40, height=20, highlightthickness=2,
                                highlightbackground="white", bd=0)
        self.preview.pack(side='right')

        # Roda de cores
        self.wheel_canvas = tk.Canvas(self.shell, width=150, height=150,
                                      bg=menu_ref.bg_color, highlightthickness=0, bd=0)
        self.wheel_canvas.pack(pady=5)
        self._render_hue_wheel()

        # Sliders de saturação e valor
        sat_frame = tk.Frame(self.shell, bg=menu_ref.bg_color)
        sat_frame.pack(fill='x', pady=2)
        tk.Label(sat_frame, text="SAT", fg="gray", bg=menu_ref.bg_color,
                font=("Arial", 7)).pack(side='left', padx=5)

        self.sat_canvas = tk.Canvas(sat_frame, height=10, highlightthickness=0, bd=0)
        self.sat_canvas.pack(side='left', fill='x', expand=True)

        val_frame = tk.Frame(self.shell, bg=menu_ref.bg_color)
        val_frame.pack(fill='x', pady=2)
        tk.Label(val_frame, text="VAL", fg="gray", bg=menu_ref.bg_color,
                font=("Arial", 7)).pack(side='left', padx=5)

        self.val_canvas = tk.Canvas(val_frame, height=10, highlightthickness=0, bd=0)
        self.val_canvas.pack(side='left', fill='x', expand=True)

        # Bindings
        self.wheel_canvas.bind("<B1-Motion>", self._pick_hue)
        self.wheel_canvas.bind("<Button-1>", self._pick_hue)
        self.sat_canvas.bind("<B1-Motion>", self._pick_sat)
        self.sat_canvas.bind("<Button-1>", self._pick_sat)
        self.val_canvas.bind("<B1-Motion>", self._pick_val)
        self.val_canvas.bind("<Button-1>", self._pick_val)

        self._update_all()

    def _render_hue_wheel(self):
        """Renderiza a roda de cores"""
        img = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        center = 75

        for y in range(150):
            for x in range(150):
                dx, dy = x - center, y - center
                dist = math.sqrt(dx*dx + dy*dy)
                if 50 < dist < 70:
                    angle = math.atan2(dy, dx) / (2 * math.pi) + 0.5
                    r, g, b = colorsys.hsv_to_rgb(angle, 1, 1)
                    draw.point((x, y), fill=(int(r*255), int(g*255), int(b*255), 255))

        self.wheel_tk = ImageTk.PhotoImage(img)
        self.wheel_canvas.create_image(75, 75, image=self.wheel_tk)
        self.cursor = self.wheel_canvas.create_oval(0, 0, 0, 0, outline="white", width=3)

    def _update_all(self):
        """Atualiza todos os componentes"""
        rgb = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        hex_c = '#%02x%02x%02x' % tuple(int(x*255) for x in rgb)
        self.preview.config(bg=hex_c)
        self.menu.data[self.var_name] = hex_c

        # Atualizar barra de saturação
        self.sat_canvas.delete("all")
        width = self.sat_canvas.winfo_width() if self.sat_canvas.winfo_width() > 1 else 150
        for i in range(width):
            r, g, b = colorsys.hsv_to_rgb(self.h, i/width, self.v)
            color = '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
            self.sat_canvas.create_line(i, 0, i, 10, fill=color)

        # Atualizar barra de valor
        self.val_canvas.delete("all")
        for i in range(width):
            r, g, b = colorsys.hsv_to_rgb(self.h, self.s, i/width)
            color = '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
            self.val_canvas.create_line(i, 0, i, 10, fill=color)

    def _pick_hue(self, e):
        """Seleciona matiz (hue)"""
        dx, dy = e.x - 75, e.y - 75
        dist = math.sqrt(dx*dx + dy*dy)

        if 50 < dist < 70:
            self.h = (math.atan2(dy, dx) / (2 * math.pi)) % 1.0
            angle = self.h * 2 * math.pi
            cursor_x = 75 + 60 * math.cos(angle)
            cursor_y = 75 + 60 * math.sin(angle)
            self.wheel_canvas.coords(self.cursor, cursor_x-4, cursor_y-4,
                                    cursor_x+4, cursor_y+4)
            self._update_all()

    def _pick_sat(self, e):
        """Seleciona saturação"""
        width = self.sat_canvas.winfo_width()
        self.s = max(0, min(e.x/width, 1.0))
        self._update_all()

    def _pick_val(self, e):
        """Seleciona valor (brightness)"""
        width = self.val_canvas.winfo_width()
        self.v = max(0, min(e.x/width, 1.0))
        self._update_all()


class ModernSlider:
    def __init__(self, container, text, de, ate, menu_ref, default=None, callback=None):
        self.de, self.ate = de, ate
        self.theme = menu_ref.theme
        self.bg = menu_ref.bg_color
        self.callback = callback
        self.current_value = default if default is not None else de

        self.shell = tk.Frame(container, bg=self.bg, pady=8, bd=0)
        self.shell.pack(fill='x', padx=30)

        # Header
        f = tk.Frame(self.shell, bg=self.bg)
        f.pack(fill='x')

        tk.Label(f, text=text, bg=self.bg, fg="white",
                font=("Arial", 8)).pack(side='left')

        self.lval = tk.Label(f, text=str(self.current_value), bg=self.bg,
                            fg=self.theme, font=("Arial", 8, "bold"))
        self.lval.pack(side='right')

        # Canvas do slider
        self.canvas = tk.Canvas(self.shell, width=320, height=20, bg=self.bg,
                               highlightthickness=0, bd=0)
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.update)
        self.canvas.bind("<Button-1>", self.update)

        # Desenhar posição inicial
        initial_pos = 10 + ((self.current_value - self.de) / (self.ate - self.de)) * 300
        self.update(None, initial_pos)

    def update(self, event, mx=None):
        """Atualiza o slider"""
        x = mx if mx is not None else event.x
        x = max(10, min(x, 310))

        self.canvas.delete("all")

        # Trilho de fundo
        self.canvas.create_line(10, 10, 310, 10, fill="#1a1a1a", width=6, capstyle='round')

        # Trilho preenchido
        self.canvas.create_line(10, 10, x, 10, fill=self.theme, width=6, capstyle='round')

        # Botão do slider
        self.canvas.create_oval(x-8, 2, x+8, 18, fill="white", outline=self.theme, width=3)

        # Calcular valor
        val = int(self.de + ((x-10)/300) * (self.ate - self.de))
        self.current_value = val
        self.lval.config(text=str(val))

        if self.callback:
            self.callback(val)

    def get_value(self):
        """Retorna o valor atual"""
        return self.current_value


class ModernCheck:
    def __init__(self, container, text, menu_ref, default=False, callback=None):
        self.marcado = default
        self.theme = menu_ref.theme
        self.bg = menu_ref.bg_color
        self.callback = callback

        self.shell = tk.Frame(container, bg=self.bg, pady=5, bd=0)
        self.shell.pack(fill='x', padx=30)

        self.canvas = tk.Canvas(self.shell, width=18, height=18, bg=self.bg,
                               highlightthickness=0, bd=0, cursor="hand2")
        self.canvas.pack(side='left')

        label = tk.Label(self.shell, text=text, bg=self.bg, fg="white",
                        font=("Arial", 9), cursor="hand2")
        label.pack(side='left', padx=10)

        self.canvas.bind("<Button-1>", lambda e: self.toggle())
        label.bind("<Button-1>", lambda e: self.toggle())

        self.draw()

    def draw(self):
        """Desenha o checkbox"""
        self.canvas.delete("all")

        if self.marcado:
            # Checkbox marcado
            self.canvas.create_rectangle(1, 1, 17, 17, outline=self.theme,
                                        width=2, fill=self.theme)
            # Checkmark
            self.canvas.create_line(5, 9, 8, 13, fill="white", width=2, capstyle='round')
            self.canvas.create_line(8, 13, 14, 6, fill="white", width=2, capstyle='round')
        else:
            # Checkbox vazio
            self.canvas.create_rectangle(1, 1, 17, 17, outline=self.theme,
                                        width=2, fill=self.bg)

    def toggle(self):
        """Alterna estado do checkbox"""
        self.marcado = not self.marcado
        self.draw()

        if self.callback:
            self.callback(self.marcado)

    def get_value(self):
        """Retorna estado atual"""
        return self.marcado


class KeyBind:
    def __init__(self, container, text, var_name, menu_ref, default="NONE"):
        self.menu = menu_ref
        self.var_name = var_name
        self.key = default
        self.listening = False

        self.shell = tk.Frame(container, bg=menu_ref.bg_color, pady=5, bd=0)
        self.shell.pack(fill='x', padx=30)

        tk.Label(self.shell, text=text, bg=menu_ref.bg_color, fg="white",
                font=("Arial", 8)).pack(side='left')

        self.btn = tk.Button(self.shell, text=self.key, bg="#1a1a1a",
                            fg=menu_ref.theme, font=("Arial", 7, "bold"),
                            bd=2, relief="solid", width=12,
                            command=self.start_listen, cursor="hand2",
                            activebackground="#2a2a2a")
        self.btn.pack(side='right')

        self.menu.data[var_name] = self.key

    def start_listen(self):
        """Inicia escuta de tecla"""
        if self.listening:
            return

        self.listening = True
        self.btn.config(text="PRESSIONE...", fg="yellow", state='disabled')
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        """Escuta por uma tecla"""
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                self.key = event.name.upper()
                self.menu.data[self.var_name] = self.key
                self.btn.config(text=self.key, fg=self.menu.theme, state='normal')
                self.listening = False
        except Exception as e:
            self.btn.config(text="ERRO", fg="red", state='normal')
            self.listening = False


class ModernButton:
    """Botão moderno com efeitos"""
    def __init__(self, container, text, menu_ref, callback=None, style="primary"):
        self.menu = menu_ref
        self.callback = callback

        colors = {
            'primary': menu_ref.theme,
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db'
        }

        color = colors.get(style, menu_ref.theme)

        self.shell = tk.Frame(container, bg=menu_ref.bg_color, pady=5, bd=0)
        self.shell.pack(fill='x', padx=30)

        self.btn = tk.Button(self.shell, text=text.upper(), bg=color, fg="white",
                            font=("Arial", 8, "bold"), bd=0, cursor="hand2",
                            command=self._on_click, activebackground=color,
                            relief='flat')
        self.btn.pack(fill='x', ipady=10)

        # Efeitos hover
        self.btn.bind("<Enter>", lambda e: self.btn.config(relief='raised'))
        self.btn.bind("<Leave>", lambda e: self.btn.config(relief='flat'))

    def _on_click(self):
        """Callback do botão"""
        if self.callback:
            self.callback()


# --- EXEMPLO DE USO ---
if __name__ == "__main__":
    # Teste do Overlay (descomente para testar)
    """
    # Criar overlay para o Bloco de Notas
    overlay = ProcessOverlay("notepad.exe", alpha=0.5)

    # Desenhar alguns elementos
    overlay.draw_rectangle(50, 50, 200, 100, color="red", thickness=3)
    overlay.draw_circle(300, 200, 50, color="lime", thickness=2)
    overlay.draw_text(150, 150, "ESP OVERLAY", color="yellow", font=("Arial", 16, "bold"))
    overlay.draw_crosshair(400, 300, size=30, color="cyan", thickness=2)

    # Iniciar overlay
    overlay.run()
    """

    # Menu principal
    menu = ClivMenu(
        title="CLIV1 EXTREME SENSE",
        theme_color="#8e44ad",
        part_color="white",
        part_count=50,
        part_speed=(0.3, 1.0)
    )

    # Aba AIMBOT
    aimbot = menu.add_tab("AIMBOT")

    ImageSeparator(aimbot, "ESP RENDER GL", menu_ref=menu)
    ModernCheck(aimbot, "Box ESP aimbot", menu, default=True,
                callback=lambda v: menu.show_notification("ESP", f"Box ESP: {'ON' if v else 'OFF'}", 2000, "info"))

    color_picker = DynamicColorPicker(aimbot, "BOX_COLOR", menu)

    fov_slider = ModernSlider(aimbot, "FOV Radius", 1, 500, menu, default=160,
                             callback=lambda v: print(f"FOV: {v}"))

    # Aba VISUALS
    visuals = menu.add_tab("VISUALS")

    ImageSeparator(visuals, "VISUAL SETTINGS", menu_ref=menu)

    graph = ModernGraph(visuals, "FPS MONITOR", menu)

    # Simular FPS variável
    def update_fps():
        import random
        fps = random.randint(50, 144)
        graph.add_value(fps)
        menu.root.after(1000, update_fps)

    menu.root.after(1000, update_fps)

    ModernCheck(visuals, "Wallhack", menu, default=False)
    ModernCheck(visuals, "No Recoil", menu, default=True)

    alpha_slider = ModernSlider(visuals, "Menu Opacity", 20, 100, menu, default=95,
                               callback=menu.set_alpha)

    # Aba MISC
    misc = menu.add_tab("MISC")

    ImageSeparator(misc, "MISCELLANEOUS", menu_ref=menu)

    audio = AudioPlayer(misc, menu)

    keybind = KeyBind(misc, "Aimbot Key", "AIMBOT_KEY", menu, default="MOUSE5")

    # Botão para testar overlay
    ModernButton(misc, "Test Overlay (Notepad)", menu,
                callback=lambda: menu.show_notification("Overlay", "Abra o Bloco de Notas e descomente o código do overlay!", 4000, "info"),
                style="info")

    ModernButton(misc, "Test Notification", menu,
                callback=lambda: menu.show_notification("Test", "Esta é uma notificação de teste!", 4000, "success"),
                style="success")

    ModernButton(misc, "Show MessageBox", menu,
                callback=lambda: menu.show_message("Informação", "Este é um messagebox personalizado!", "info"),
                style="info")

    ModernButton(misc, "Warning Test", menu,
                callback=lambda: menu.show_notification("Aviso", "Isto é um aviso importante!", 5000, "warning"),
                style="warning")

    ModernButton(misc, "Error Test", menu,
                callback=lambda: menu.show_notification("Erro", "Ocorreu um erro no sistema!", 5000, "error"),
                style="danger")

    # Teste de múltiplas notificações
    ModernButton(misc, "Spam Notifications (5x)", menu,
                callback=lambda: [menu.show_notification(f"Notif {i+1}", f"Mensagem de teste número {i+1}", 4000, ["info", "success", "warning"][i%3]) for i in range(5)],
                style="warning")

    menu.run("insert")
