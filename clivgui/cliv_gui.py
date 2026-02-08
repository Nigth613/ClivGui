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
from typing import Optional, Callable, Tuple, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class WidgetStyle:
    """Estilo configurável para widgets"""
    x: int = 0
    y: int = 0
    width: Optional[int] = None
    height: Optional[int] = None
    bg_color: str = "#1a1a1a"
    fg_color: str = "white"
    border_radius: int = 0
    border_width: int = 0
    border_color: str = "#555555"
    padding: Tuple[int, int, int, int] = (10, 10, 10, 10)  # top, right, bottom, left
    margin: Tuple[int, int, int, int] = (5, 5, 5, 5)
    font: Tuple[str, int, str] = ("Arial", 9, "normal")
    anchor: str = "nw"  # nw, n, ne, w, center, e, sw, s, se
    pack: bool = True  # Se False, usa place() com x, y


class ProcessOverlay:
    """Overlay transparente que acompanha a janela de um processo"""

    def __init__(self, process_name: str, bg_color: str = "#000000", alpha: float = 0.3):
        """
        Args:
            process_name: Nome do processo (ex: "notepad.exe" ou "chrome.exe")
            bg_color: Cor de fundo do overlay
            alpha: Transparência (0.0 a 1.0)
        """
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("Alpha deve estar entre 0.0 e 1.0")

        self.process_name = process_name
        self.hwnd = None
        self.running = False
        self.alpha = alpha

        try:
            self.root = tk.Tk()
            self.root.overrideredirect(True)
            self.root.attributes("-topmost", True)
            self.root.attributes("-transparentcolor", bg_color)
            self.root.attributes("-alpha", alpha)
            self.root.config(bg=bg_color)

            self.canvas = tk.Canvas(
                self.root,
                bg=bg_color,
                highlightthickness=0,
                bd=0
            )
            self.canvas.pack(fill='both', expand=True)
            self.drawings = []
        except Exception as e:
            raise RuntimeError(f"Erro ao inicializar overlay: {e}")

    def find_process_window(self) -> Optional[int]:
        """Encontra a janela do processo pelo nome"""
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    process = psutil.Process(pid)
                    if process.name().lower() == self.process_name.lower():
                        hwnds.append(hwnd)
                except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
                    pass
            return True

        hwnds = []
        try:
            win32gui.EnumWindows(callback, hwnds)
        except Exception:
            return None
        return hwnds[0] if hwnds else None

    def get_window_rect(self, hwnd: int) -> Optional[Tuple[int, int, int, int]]:
        """Obtém posição e tamanho da janela"""
        try:
            rect = win32gui.GetWindowRect(hwnd)
            x, y = rect[0], rect[1]
            w = rect[2] - rect[0]
            h = rect[3] - rect[1]
            return x, y, w, h
        except Exception:
            return None

    def update_position(self):
        """Atualiza posição do overlay para seguir a janela do processo"""
        if not self.running:
            return

        try:
            if not self.hwnd:
                self.hwnd = self.find_process_window()

            if self.hwnd:
                if not win32gui.IsWindow(self.hwnd):
                    self.hwnd = self.find_process_window()

                if self.hwnd:
                    rect = self.get_window_rect(self.hwnd)
                    if rect:
                        x, y, w, h = rect
                        self.root.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            self.hwnd = None

        if self.running:
            self.root.after(16, self.update_position)

    def draw_rectangle(self, x: int, y: int, width: int, height: int,
                      color: str = "red", thickness: int = 2,
                      fill: Optional[str] = None) -> int:
        """Desenha um retângulo no overlay"""
        rect_id = self.canvas.create_rectangle(
            x, y, x + width, y + height,
            outline=color,
            width=thickness,
            fill=fill if fill else ""
        )
        self.drawings.append(rect_id)
        return rect_id

    def draw_line(self, x1: int, y1: int, x2: int, y2: int,
                  color: str = "red", thickness: int = 2) -> int:
        """Desenha uma linha no overlay"""
        line_id = self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=thickness
        )
        self.drawings.append(line_id)
        return line_id

    def draw_circle(self, x: int, y: int, radius: int,
                    color: str = "red", thickness: int = 2,
                    fill: Optional[str] = None) -> int:
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

    def draw_text(self, x: int, y: int, text: str,
                  color: str = "white",
                  font: Tuple[str, int, str] = ("Arial", 12, "bold")) -> int:
        """Desenha texto no overlay"""
        text_id = self.canvas.create_text(
            x, y,
            text=text,
            fill=color,
            font=font
        )
        self.drawings.append(text_id)
        return text_id

    def draw_crosshair(self, x: int, y: int, size: int = 20,
                       color: str = "lime", thickness: int = 2):
        """Desenha uma mira (crosshair) no overlay"""
        self.draw_line(x - size, y, x + size, y, color, thickness)
        self.draw_line(x, y - size, x, y + size, color, thickness)

    def clear_drawings(self):
        """Limpa todos os desenhos"""
        for drawing_id in self.drawings:
            try:
                self.canvas.delete(drawing_id)
            except Exception:
                pass
        self.drawings.clear()

    def delete_drawing(self, drawing_id: int):
        """Remove um desenho específico"""
        try:
            self.canvas.delete(drawing_id)
            if drawing_id in self.drawings:
                self.drawings.remove(drawing_id)
        except Exception:
            pass

    def set_alpha(self, alpha: float):
        """Define a transparência do overlay (0.0 a 1.0)"""
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("Alpha deve estar entre 0.0 e 1.0")
        self.alpha = alpha
        self.root.attributes("-alpha", self.alpha)

    def start(self) -> bool:
        """Inicia o overlay"""
        self.running = True
        self.hwnd = self.find_process_window()

        if not self.hwnd:
            print(f"Processo '{self.process_name}' não encontrado!")
            return False

        self.update_position()
        return True

    def stop(self):
        """Para o overlay"""
        self.running = False
        try:
            self.root.destroy()
        except Exception:
            pass

    def run(self):
        """Inicia o loop principal do overlay"""
        if self.start():
            self.root.mainloop()


class NotificationManager:
    """Gerenciador de notificações estilo Roblox"""

    def __init__(self):
        self.notifications: List[tk.Toplevel] = []
        self.notification_windows: List[tk.Toplevel] = []
        self.lock = threading.Lock()

    def show(self, title: str, message: str, duration: int = 3000,
             notification_type: str = "info") -> tk.Toplevel:
        """
        Mostra uma notificação no canto inferior direito

        Args:
            title: Título da notificação
            message: Mensagem da notificação
            duration: Duração em milissegundos
            notification_type: Tipo ('info', 'success', 'warning', 'error')
        """
        colors = {
            'info': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'error': '#e74c3c'
        }

        color = colors.get(notification_type, '#3498db')

        try:
            notif = tk.Toplevel()
            notif.overrideredirect(True)
            notif.attributes("-topmost", True)
            notif.attributes("-alpha", 0.0)

            screen_width = notif.winfo_screenwidth()
            screen_height = notif.winfo_screenheight()

            width = 320
            height = 90

            with self.lock:
                offset = len(self.notification_windows) * (height + 10)

            x = screen_width - width - 20
            y = screen_height - height - 60 - offset

            notif.geometry(f"{width}x{height}+{x}+{y}")

            main_frame = tk.Frame(notif, bg=color, bd=0)
            main_frame.pack(fill='both', expand=True, padx=2, pady=2)

            inner_frame = tk.Frame(main_frame, bg="#1a1a1a", bd=0)
            inner_frame.pack(fill='both', expand=True)

            header = tk.Frame(inner_frame, bg=color, height=30, bd=0)
            header.pack(fill='x', side='top')
            header.pack_propagate(False)

            tk.Label(header, text=title.upper(), bg=color, fg="white",
                    font=("Arial", 9, "bold")).pack(side='left', padx=10, pady=5)

            close_btn = tk.Label(header, text="✕", bg=color, fg="white",
                                font=("Arial", 10), cursor="hand2")
            close_btn.pack(side='right', padx=10)
            close_btn.bind("<Button-1>", lambda e: self._close_notification(notif))

            msg_frame = tk.Frame(inner_frame, bg="#1a1a1a", bd=0)
            msg_frame.pack(fill='both', expand=True, padx=10, pady=5)

            tk.Label(msg_frame, text=message, bg="#1a1a1a", fg="white",
                    font=("Arial", 8), wraplength=280, justify='left').pack(anchor='w')

            progress_canvas = tk.Canvas(inner_frame, height=3, bg="#1a1a1a",
                                       highlightthickness=0, bd=0)
            progress_canvas.pack(fill='x', side='bottom')

            progress_bar = progress_canvas.create_rectangle(0, 0, width, 3,
                                                            fill=color, outline="")

            with self.lock:
                self.notification_windows.append(notif)

            self._animate_in(notif, x, y, width)
            self._start_progress_fixed(notif, progress_canvas, progress_bar,
                                       duration, width, color)

            return notif
        except Exception as e:
            print(f"Erro ao criar notificação: {e}")
            return None

    def _start_progress_fixed(self, window: tk.Toplevel, canvas: tk.Canvas,
                             bar: int, duration: int, width: int, color: str):
        """Anima a barra de progresso"""
        start_time = time.time()
        closed = {'value': False}
        after_ids = []

        def update():
            if closed['value']:
                return

            try:
                if not window.winfo_exists():
                    closed['value'] = True
                    return
            except Exception:
                closed['value'] = True
                return

            elapsed = (time.time() - start_time) * 1000
            progress = min(elapsed / duration, 1.0)

            try:
                remaining_width = width * (1 - progress)
                canvas.coords(bar, 0, 0, remaining_width, 3)
            except Exception:
                closed['value'] = True
                return

            if progress < 1.0:
                after_id = window.after(16, update)
                after_ids.append(after_id)
            else:
                closed['value'] = True
                self._close_notification(window)

        def cancel_updates():
            closed['value'] = True
            for after_id in after_ids:
                try:
                    window.after_cancel(after_id)
                except Exception:
                    pass

        window.cancel_progress = cancel_updates
        update()

    def _animate_in(self, window: tk.Toplevel, target_x: int,
                    target_y: int, width: int):
        """Animação de entrada (slide da direita + fade)"""
        start_x = target_x + width
        steps = 15
        delay = 15

        def animate(step=0):
            try:
                if not window.winfo_exists():
                    return

                if step <= steps:
                    progress = step / steps
                    current_x = start_x - (start_x - target_x) * self._ease_out_cubic(progress)
                    alpha = progress * 0.95

                    window.geometry(f"+{int(current_x)}+{target_y}")
                    window.attributes("-alpha", alpha)

                    window.after(delay, lambda: animate(step + 1))
            except Exception:
                pass

        animate()

    def _animate_out(self, window: tk.Toplevel, callback: Optional[Callable] = None):
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
                except Exception:
                    if callback:
                        callback()

            animate()
        except Exception:
            if callback:
                callback()

    @staticmethod
    def _ease_out_cubic(t: float) -> float:
        """Easing function para animação suave"""
        return 1 - pow(1 - t, 3)

    @staticmethod
    def _ease_in_cubic(t: float) -> float:
        """Easing function para animação suave"""
        return t * t * t

    def _close_notification(self, window: tk.Toplevel):
        """Fecha a notificação com animação"""
        try:
            if not window.winfo_exists():
                return
        except Exception:
            return

        if hasattr(window, 'cancel_progress'):
            try:
                window.cancel_progress()
            except Exception:
                pass

        with self.lock:
            if window in self.notification_windows:
                self.notification_windows.remove(window)

        def destroy():
            try:
                if window.winfo_exists():
                    window.destroy()
            except Exception:
                pass

            if self.notification_windows:
                try:
                    valid_windows = [w for w in self.notification_windows
                                   if self._is_window_valid(w)]
                    if valid_windows:
                        valid_windows[0].after(50, self._reposition_notifications)
                except Exception:
                    pass

        self._animate_out(window, destroy)

    @staticmethod
    def _is_window_valid(window: tk.Toplevel) -> bool:
        """Verifica se janela ainda é válida"""
        try:
            return window.winfo_exists()
        except Exception:
            return False

    def _reposition_notifications(self):
        """Reposiciona notificações após fechamento"""
        try:
            with self.lock:
                self.notification_windows = [w for w in self.notification_windows
                                           if self._is_window_valid(w)]

                if not self.notification_windows:
                    return

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

                            self._smooth_move(notif, y)
                    except Exception:
                        continue
        except Exception:
            pass

    def _smooth_move(self, window: tk.Toplevel, target_y: int):
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
        except Exception:
            pass


class MessageBox:
    """MessageBox personalizado estilo CLIV"""

    @staticmethod
    def show(title: str, message: str, msg_type: str = "info",
             theme_color: str = "#8e44ad") -> None:
        """
        Mostra um messagebox personalizado

        Args:
            title: Título da janela
            message: Mensagem a ser exibida
            msg_type: Tipo ('info', 'success', 'warning', 'error', 'question')
            theme_color: Cor do tema
        """
        try:
            box = tk.Toplevel()
            box.overrideredirect(True)
            box.geometry("420x220")
            box.configure(bg="#05050a")
            box.attributes("-topmost", True)

            box.update_idletasks()
            x = (box.winfo_screenwidth() // 2) - (420 // 2)
            y = (box.winfo_screenheight() // 2) - (220 // 2)
            box.geometry(f"420x220+{x}+{y}")

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

            header = tk.Frame(box, bg=color, height=35, bd=0)
            header.pack(fill='x', side='top')
            header.pack_propagate(False)

            title_frame = tk.Frame(header, bg=color)
            title_frame.pack(side='left', fill='y', padx=10)

            tk.Label(title_frame, text=icon, bg=color, fg="white",
                    font=("Arial", 14, "bold")).pack(side='left', padx=(0, 8))
            tk.Label(title_frame, text=title.upper(), bg=color, fg="white",
                    font=("Impact", 10)).pack(side='left')

            close_btn = tk.Button(header, text="✕", command=box.destroy,
                                 bg=color, fg="white", bd=0, width=5,
                                 activebackground="#ff4444", cursor="hand2",
                                 font=("Arial", 10))
            close_btn.pack(side='right', fill='y')

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

            body = tk.Frame(box, bg="#05050a", bd=0)
            body.pack(fill='both', expand=True, padx=25, pady=20)

            msg_label = tk.Label(body, text=message, bg="#05050a", fg="white",
                                font=("Arial", 9), wraplength=370, justify='left')
            msg_label.pack(expand=True)

            btn_frame = tk.Frame(box, bg="#05050a", bd=0)
            btn_frame.pack(fill='x', padx=25, pady=(0, 20))

            ok_btn = tk.Button(btn_frame, text="OK", bg=color, fg="white",
                              font=("Arial", 9, "bold"), bd=0, width=18,
                              command=box.destroy, cursor="hand2",
                              activebackground=color, activeforeground="white",
                              relief='flat')
            ok_btn.pack(side='right', ipady=8)

            def on_enter(e):
                ok_btn.config(relief='raised')

            def on_leave(e):
                ok_btn.config(relief='flat')

            ok_btn.bind("<Enter>", on_enter)
            ok_btn.bind("<Leave>", on_leave)

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
        except Exception as e:
            print(f"Erro ao mostrar messagebox: {e}")


class ClivMenu:
    """Menu principal CLIV melhorado"""

    def __init__(self, title: str = "CLIV1 EXTREME", theme_color: str = "#8e44ad",
                 bg_img_path: Optional[str] = None, width: int = 450, height: int = 720,
                 part_color: str = "white", part_count: int = 40,
                 part_speed: Tuple[float, float] = (0.2, 0.8),
                 enable_tray_icon: bool = False, tray_icon_path: Optional[str] = None,
                 enable_tabs: bool = True):
        """
        Inicializa o menu CLIV

        Args:
            title: Título da janela
            theme_color: Cor do tema
            bg_img_path: Caminho para imagem de fundo
            width: Largura da janela
            height: Altura da janela
            part_color: Cor das partículas
            part_count: Quantidade de partículas
            part_speed: Range de velocidade das partículas
            enable_tray_icon: Habilita ícone na bandeja
            tray_icon_path: Caminho para ícone da bandeja
            enable_tabs: Habilita sistema de abas
        """
        self.root = tk.Tk()
        self.theme = theme_color
        self.bg_color = "#05050a"
        self.data: Dict[str, Any] = {}
        self.abas: Dict[str, Dict] = {}
        self.botoes_abas: Dict[str, tk.Button] = {}
        self.aba_atual: Optional[str] = None
        self.aberto = True
        self.bg_img_path = bg_img_path
        self.title = title
        self.width = width
        self.height = height
        self.enable_tabs = enable_tabs

        self.p_color = part_color
        self.p_count = part_count
        self.p_speed_range = part_speed

        self.notif_manager = NotificationManager()

        self.enable_tray = enable_tray_icon
        self.tray_icon_path = tray_icon_path
        self.tray_icon = None
        self.tray_thread = None

        # Container principal direto (sem abas por padrão)
        self.main_container = None

        try:
            pygame.mixer.init()
        except Exception:
            pass

        self._setup_main_ui(title)
        self._init_particles()

        if self.enable_tray:
            self._init_tray_icon()

    def _setup_main_ui(self, title: str):
        """Configura a interface principal"""
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg=self.bg_color)

        # Canvas de fundo
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0,
                                   bg=self.bg_color, bd=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Carregar imagem de fundo se especificada
        if self.bg_img_path and os.path.exists(self.bg_img_path):
            try:
                img = Image.open(self.bg_img_path).resize(
                    (self.width, self.height), Image.Resampling.LANCZOS
                )
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

        min_btn = tk.Button(self.header, text="−", command=self.toggle_visibility,
                           bg=self.theme, fg="white", bd=0, width=5,
                           activebackground="#555", cursor="hand2")
        min_btn.pack(side='right', fill='y')

        close_btn = tk.Button(self.header, text="✕", command=self._on_close,
                             bg=self.theme, fg="white", bd=0, width=5,
                             activebackground="#ff4444", cursor="hand2")
        close_btn.pack(side='right', fill='y')

        self.header.bind("<Button-1>", self._start_move)
        self.header.bind("<B1-Motion>", self._on_move)

        # Barra de abas (opcional)
        if self.enable_tabs:
            self.tab_bar = tk.Frame(self.root, bg="#000", height=35, bd=0)
            self.tab_bar.pack(fill='x', side='top')
            self.tab_bar.pack_propagate(False)

            self.container_principal = tk.Frame(self.root, bg=self.bg_color, bd=0)
            self.container_principal.place(x=0, y=70, width=self.width,
                                         height=self.height - 70)
        else:
            self.tab_bar = None
            # Container principal sem abas
            self.container_principal = tk.Frame(self.root, bg=self.bg_color, bd=0)
            self.container_principal.place(x=0, y=35, width=self.width,
                                         height=self.height - 35)

            # Criar container scrollável direto
            self.main_container = self._create_scrollable_container(
                self.container_principal
            )

    def _create_scrollable_container(self, parent: tk.Frame) -> tk.Frame:
        """Cria um container com scroll"""
        frame_container = tk.Frame(parent, bg=self.bg_color, bd=0)
        frame_container.pack(fill='both', expand=True)

        canvas = tk.Canvas(frame_container, bg=self.bg_color,
                          highlightthickness=0, bd=0)

        scrollbar_frame = tk.Frame(frame_container, bg=self.bg_color,
                                  width=8, bd=0)
        scrollbar_canvas = tk.Canvas(scrollbar_frame, bg="#0a0a15", width=8,
                                    highlightthickness=0, bd=0)
        scrollbar_canvas.pack(fill='both', expand=True)

        scroll_data = {
            'dragging': False,
            'start_y': 0,
            'thumb': None,
            'thumb_y': 0,
            'thumb_height': 100
        }

        def update_scrollbar(*args):
            try:
                first, last = canvas.yview()
                canvas_height = scrollbar_canvas.winfo_height()

                if canvas_height < 10:
                    return

                visible_ratio = last - first
                thumb_height = max(30, canvas_height * visible_ratio)
                thumb_y = first * canvas_height

                scrollbar_canvas.delete("all")

                scrollbar_canvas.create_rectangle(
                    1, 0, 7, canvas_height,
                    fill="#0a0a15", outline=""
                )

                scrollbar_canvas.create_rectangle(
                    1, thumb_y, 7, thumb_y + thumb_height,
                    fill=self.theme, outline="", tags="thumb"
                )

                scroll_data['thumb_height'] = thumb_height
                scroll_data['thumb_y'] = thumb_y

            except Exception:
                pass

        def on_scroll_click(event):
            scroll_data['dragging'] = True
            scroll_data['start_y'] = event.y

        def on_scroll_drag(event):
            if scroll_data['dragging']:
                canvas_height = scrollbar_canvas.winfo_height()
                if canvas_height < 10:
                    return

                delta = event.y - scroll_data['start_y']
                new_y = scroll_data['thumb_y'] + delta

                max_y = canvas_height - scroll_data['thumb_height']
                new_y = max(0, min(new_y, max_y))

                fraction = new_y / canvas_height
                canvas.yview_moveto(fraction)
                scroll_data['start_y'] = event.y

        def on_scroll_release(event):
            scroll_data['dragging'] = False

        scrollbar_canvas.bind("<Button-1>", on_scroll_click)
        scrollbar_canvas.bind("<B1-Motion>", on_scroll_drag)
        scrollbar_canvas.bind("<ButtonRelease-1>", on_scroll_release)

        canvas.configure(yscrollcommand=lambda f, l: (update_scrollbar(f, l), None)[-1])

        scrollable_frame = tk.Frame(canvas, bg=self.bg_color, bd=0)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: (canvas.configure(scrollregion=canvas.bbox("all")),
                      update_scrollbar())
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                update_scrollbar()
            except Exception:
                pass

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        scrollbar_frame.pack(side="right", fill="y", padx=(2, 0))
        canvas.pack(side="left", fill="both", expand=True)

        frame_container.after(100, update_scrollbar)

        return scrollable_frame

    def _init_particles(self):
        """Inicializa sistema de partículas"""
        self.particles = []
        for _ in range(self.p_count):
            self.particles.append({
                'id': self.bg_canvas.create_oval(0, 0, 2, 2, fill=self.p_color, outline=""),
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(self.p_speed_range[0], self.p_speed_range[1]),
                'opacity': random.uniform(0.3, 1.0)
            })
        self._update_particles()

    def _init_tray_icon(self):
        """Inicializa o ícone na system tray"""
        try:
            from pystray import Icon, Menu, MenuItem

            if self.tray_icon_path and os.path.exists(self.tray_icon_path):
                icon_image = Image.open(self.tray_icon_path)
            else:
                icon_image = self._create_default_icon()

            menu = Menu(
                MenuItem('Mostrar/Ocultar', self.toggle_visibility, default=True),
                MenuItem('Notificação de Teste', self._tray_test_notification),
                Menu.SEPARATOR,
                MenuItem('Fechar', self._tray_quit)
            )

            self.tray_icon = Icon(
                name=self.title,
                icon=icon_image,
                title=self.title,
                menu=menu
            )

            self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            self.tray_thread.start()

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

    def _create_default_icon(self) -> Image.Image:
        """Cria um ícone padrão"""
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        hex_color = self.theme.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        draw.ellipse([4, 4, 60, 60], fill=rgb, outline=(255, 255, 255))

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
        """Atualiza partículas"""
        if not self.aberto or not self.root.winfo_exists():
            return

        try:
            for p in self.particles:
                p['y'] -= p['speed']
                if p['y'] < 0:
                    p['y'] = self.height
                    p['x'] = random.randint(0, self.width)

                self.bg_canvas.coords(p['id'], p['x'], p['y'],
                                     p['x']+2, p['y']+2)

            self.root.after(30, self._update_particles)
        except Exception:
            pass

    def get_container(self) -> tk.Frame:
        """
        Retorna o container principal para adicionar widgets.
        Se tabs estiverem desabilitadas, retorna o container direto.
        Se tabs estiverem habilitadas mas nenhuma foi criada, cria uma aba padrão.
        """
        if not self.enable_tabs:
            return self.main_container

        # Se tabs estão habilitadas mas nenhuma existe, criar uma padrão
        if not self.abas:
            return self.add_tab("Main")

        # Retornar a aba atual ou a primeira disponível
        if self.aba_atual and self.aba_atual in self.abas:
            return self.abas[self.aba_atual]['frame']

        first_tab = next(iter(self.abas))
        return self.abas[first_tab]['frame']

    def add_tab(self, name: str) -> tk.Frame:
        """Adiciona uma nova aba ao menu (apenas se tabs estiverem habilitadas)"""
        if not self.enable_tabs:
            raise RuntimeError("Tabs não estão habilitadas neste menu. "
                             "Use get_container() para obter o container principal.")

        frame_container = self._create_scrollable_container(self.container_principal)

        self.abas[name] = {
            'container': frame_container.master.master,  # Frame principal
            'frame': frame_container,  # Frame scrollável
        }

        btn = tk.Button(self.tab_bar, text=name.upper(), bg="#000", fg="gray",
                        activeforeground=self.theme, font=("Arial", 7, "bold"),
                        bd=0, command=lambda n=name: self.show_tab(n),
                        activebackground="#111", cursor="hand2", relief='flat')
        btn.pack(side='left', expand=True, fill='both')
        self.botoes_abas[name] = btn

        if not self.aba_atual:
            self.show_tab(name)

        return frame_container

    def show_tab(self, name: str):
        """Mostra a aba selecionada"""
        if not self.enable_tabs:
            return

        for n, tab_data in self.abas.items():
            tab_data['container'].pack_forget()
            self.botoes_abas[n].config(fg="gray", relief='flat')

        self.abas[name]['container'].pack(fill='both', expand=True)
        self.botoes_abas[name].config(fg=self.theme, relief='sunken')
        self.aba_atual = name

    def set_alpha(self, val: float):
        """Define transparência da janela (0-100)"""
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
            if self.tray_icon:
                try:
                    self.tray_icon.stop()
                except Exception:
                    pass

            for notif in list(self.notif_manager.notification_windows):
                try:
                    if notif.winfo_exists():
                        if hasattr(notif, 'cancel_progress'):
                            notif.cancel_progress()
                        notif.destroy()
                except Exception:
                    pass

            self.notif_manager.notification_windows.clear()

            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

            self.root.quit()
            self.root.destroy()
        except Exception:
            pass

    def show_notification(self, title: str, message: str,
                         duration: int = 3000, notif_type: str = "info"):
        """Mostra notificação no canto da tela"""
        self.notif_manager.show(title, message, duration, notif_type)

    def show_message(self, title: str, message: str, msg_type: str = "info"):
        """Mostra messagebox personalizado"""
        MessageBox.show(title, message, msg_type, self.theme)

    def run(self, hotkey: str = "insert"):
        """Inicia o loop principal"""
        try:
            keyboard.add_hotkey(hotkey, self.toggle_visibility)
        except Exception as e:
            print(f"Erro ao registrar hotkey: {e}")

        self.root.after(500, lambda: self.show_notification(
            "Menu Iniciado",
            f"Pressione {hotkey.upper()} para mostrar/ocultar",
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
        except Exception:
            pass


# ============================================================================
# WIDGETS INDEPENDENTES COM ESTILO CONFIGURÁVEL
# ============================================================================

class AudioPlayer:
    """Player de áudio integrado"""

    def __init__(self, container: tk.Frame, menu_ref: ClivMenu,
                 audio_path: str = "music.mp3", autoplay: bool = False,
                 loop: bool = True, style: Optional[WidgetStyle] = None):
        """
        Inicializa o player de áudio

        Args:
            container: Container pai
            menu_ref: Referência ao menu CLIV
            audio_path: Caminho do arquivo de áudio
            autoplay: Reproduzir automaticamente
            loop: Repetir em loop
            style: Estilo customizado
        """
        self.menu = menu_ref
        self.audio_path = audio_path
        self.playing = False
        self.loop = loop
        self.volume = 0.5

        if style is None:
            style = WidgetStyle()

        self.shell = tk.Frame(container, bg=style.bg_color,
                             pady=style.padding[0], bd=0)

        if style.pack:
            self.shell.pack(fill='x', padx=style.padding[3], pady=style.margin[0])
        else:
            self.shell.place(x=style.x, y=style.y, width=style.width, height=style.height)

        header_frame = tk.Frame(self.shell, bg=style.bg_color)
        header_frame.pack(fill='x', pady=(0, 10))

        tk.Label(header_frame, text="🎵 AUDIO PLAYER", fg=menu_ref.theme,
                bg=style.bg_color, font=style.font).pack(side='left')

        self.status_label = tk.Label(header_frame, text="●", fg="red",
                                     bg=style.bg_color, font=("Arial", 8))
        self.status_label.pack(side='right', padx=5)

        controls_frame = tk.Frame(self.shell, bg=style.bg_color)
        controls_frame.pack(fill='x')

        self.play_btn = tk.Button(controls_frame, text="▶", bg=menu_ref.theme,
                                  fg="white", font=("Arial", 12, "bold"), bd=0,
                                  command=self.toggle_play, cursor="hand2", width=4,
                                  activebackground=menu_ref.theme, relief='flat')
        self.play_btn.pack(side='left', padx=2, ipady=5)

        self.stop_btn = tk.Button(controls_frame, text="⏹", bg="#555",
                                  fg="white", font=("Arial", 12, "bold"), bd=0,
                                  command=self.stop_music, cursor="hand2", width=4,
                                  activebackground="#444", relief='flat')
        self.stop_btn.pack(side='left', padx=2, ipady=5)

        self.loop_btn = tk.Button(controls_frame, text="🔁",
                                  bg=menu_ref.theme if loop else "#555",
                                  fg="white", font=("Arial", 10, "bold"), bd=0,
                                  command=self.toggle_loop, cursor="hand2", width=4,
                                  activebackground=menu_ref.theme, relief='flat')
        self.loop_btn.pack(side='left', padx=2, ipady=5)

        vol_frame = tk.Frame(self.shell, bg=style.bg_color)
        vol_frame.pack(fill='x', pady=(10, 0))

        tk.Label(vol_frame, text="🔊", bg=style.bg_color, fg="white",
                font=("Arial", 10)).pack(side='left', padx=(0, 5))

        self.vol_canvas = tk.Canvas(vol_frame, height=8, bg=style.bg_color,
                                    highlightthickness=0, bd=0)
        self.vol_canvas.pack(side='left', fill='x', expand=True)

        self.vol_label = tk.Label(vol_frame, text="50%", bg=style.bg_color,
                                 fg=menu_ref.theme, font=("Arial", 8, "bold"),
                                 width=4)
        self.vol_label.pack(side='right', padx=(5, 0))

        self.vol_canvas.bind("<Button-1>", self.set_volume)
        self.vol_canvas.bind("<B1-Motion>", self.set_volume)

        self.shell.after(100, self.update_volume_bar)

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
            self.vol_canvas.create_rectangle(0, 2, width, 6, fill="#1a1a1a", outline="")

            vol_width = int(width * self.volume)
            self.vol_canvas.create_rectangle(0, 2, vol_width, 6,
                                            fill=self.menu.theme, outline="")
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
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

        if self.playing:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.play(-1 if self.loop else 0)
            except Exception:
                pass

    def set_audio_file(self, path: str):
        """Define um novo arquivo de áudio"""
        was_playing = self.playing

        if self.playing:
            self.stop_music()

        self.audio_path = path

        if was_playing and os.path.exists(path):
            self.play_music()

    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual"""
        return {
            'playing': self.playing,
            'loop': self.loop,
            'volume': self.volume,
            'file': self.audio_path
        }


class ImageSeparator:
    """Separador visual com ícone opcional"""

    def __init__(self, container: tk.Frame, text: str,
                 icon_path: Optional[str] = None, menu_ref: Optional[ClivMenu] = None,
                 style: Optional[WidgetStyle] = None):
        """
        Cria um separador visual

        Args:
            container: Container pai
            text: Texto do separador
            icon_path: Caminho para ícone opcional
            menu_ref: Referência ao menu
            style: Estilo customizado
        """
        if style is None:
            style = WidgetStyle()

        theme = menu_ref.theme if menu_ref else "#8e44ad"
        bg = menu_ref.bg_color if menu_ref else style.bg_color

        self.shell = tk.Frame(container, bg=bg, pady=style.padding[0],
                             bd=0, highlightthickness=0)

        if style.pack:
            self.shell.pack(fill='x', padx=style.padding[3])
        else:
            self.shell.place(x=style.x, y=style.y, width=style.width, height=style.height)

        if icon_path and os.path.exists(icon_path):
            try:
                img = Image.open(icon_path).resize((16, 16), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                tk.Label(self.shell, image=self.photo, bg=bg).pack(side='left', padx=5)
            except Exception:
                pass

        tk.Label(self.shell, text=text.upper(), fg=theme, bg=bg,
                font=style.font).pack(side='left')
        tk.Frame(self.shell, bg=theme, height=2, bd=0).pack(fill='x',
                                                            side='bottom', pady=2)


class ModernGraph:
    """Gráfico de linhas moderno"""

    def __init__(self, container: tk.Frame, label: str, menu_ref: ClivMenu,
                 style: Optional[WidgetStyle] = None, max_values: int = 50):
        """
        Cria um gráfico de linhas

        Args:
            container: Container pai
            label: Label do gráfico
            menu_ref: Referência ao menu
            style: Estilo customizado
            max_values: Número máximo de valores exibidos
        """
        self.menu = menu_ref
        self.values = [0] * max_values
        self.max_values = max_values

        if style is None:
            style = WidgetStyle()

        self.shell = tk.Frame(container, bg=style.bg_color,
                             pady=style.padding[0], bd=0)

        if style.pack:
            self.shell.pack(fill='x', padx=style.padding[3])
        else:
            self.shell.place(x=style.x, y=style.y, width=style.width, height=style.height)

        tk.Label(self.shell, text=label, fg=menu_ref.theme, bg=style.bg_color,
                font=style.font).pack(anchor="w")

        canvas_width = style.width if style.width else 350
        canvas_height = style.height if style.height else 60

        self.canvas = tk.Canvas(self.shell, width=canvas_width, height=canvas_height,
                               bg="#0a0a15", highlightthickness=1,
                               highlightbackground="#222", bd=0)
        self.canvas.pack()
        self.update_graph()

    def add_value(self, val: float):
        """Adiciona um valor ao gráfico"""
        self.values.pop(0)
        self.values.append(val)
        self.update_graph()

    def update_graph(self):
        """Atualiza o gráfico"""
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 350
        canvas_height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 60

        # Grid
        for i in range(0, canvas_height + 1, 20):
            self.canvas.create_line(0, i, canvas_width, i, fill="#1a1a2e", dash=(2, 4))

        # Plot
        points = []
        spacing = canvas_width / len(self.values)

        for i, v in enumerate(self.values):
            x = i * spacing
            y = canvas_height - min(v, 120) * (canvas_height / 120)
            points.append((x, y))

        if len(points) > 1:
            for i in range(len(points)-1):
                x1, y1 = points[i]
                x2, y2 = points[i+1]
                self.canvas.create_line(x1, y1, x2, y2, fill=self.menu.theme,
                                       width=2, tags="plot", smooth=True)
                self.canvas.create_polygon(x1, y1, x2, y2, x2, canvas_height,
                                          x1, canvas_height,
                                          fill=self.menu.theme, outline="",
                                          stipple="gray50", tags="fill")

            self.canvas.tag_raise("plot")


class DynamicColorPicker:
    """Seletor de cores dinâmico com roda HSV"""

    def __init__(self, container: tk.Frame, var_name: str, menu_ref: ClivMenu,
                 style: Optional[WidgetStyle] = None,
                 callback: Optional[Callable[[str], None]] = None):
        """
        Cria um seletor de cores

        Args:
            container: Container pai
            var_name: Nome da variável para armazenar a cor
            menu_ref: Referência ao menu
            style: Estilo customizado
            callback: Função chamada quando a cor muda
        """
        self.menu = menu_ref
        self.var_name = var_name
        self.h, self.s, self.v = 0.0, 1.0, 1.0
        self.callback = callback

        if style is None:
            style = WidgetStyle()

        self.shell = tk.Frame(container, bg=style.bg_color,
                             pady=style.padding[0], bd=0)

        if style.pack:
            self.shell.pack(fill='x', padx=style.padding[3])
        else:
            self.shell.place(x=style.x, y=style.y, width=style.width, height=style.height)

        head = tk.Frame(self.shell, bg=style.bg_color)
        head.pack(fill='x', pady=5)

        tk.Label(head, text=var_name.upper(), fg="white", bg=style.bg_color,
                font=style.font).pack(side='left')

        self.preview = tk.Canvas(head, width=40, height=20, highlightthickness=2,
                                highlightbackground="white", bd=0)
        self.preview.pack(side='right')

        self.wheel_canvas = tk.Canvas(self.shell, width=150, height=150,
                                      bg=style.bg_color, highlightthickness=0, bd=0)
        self.wheel_canvas.pack(pady=5)
        self._render_hue_wheel()

        # Saturação
        sat_frame = tk.Frame(self.shell, bg=style.bg_color)
        sat_frame.pack(fill='x', pady=2)
        tk.Label(sat_frame, text="SAT", fg="gray", bg=style.bg_color,
                font=("Arial", 7)).pack(side='left', padx=5)

        self.sat_canvas = tk.Canvas(sat_frame, height=10, highlightthickness=0, bd=0)
        self.sat_canvas.pack(side='left', fill='x', expand=True)

        # Valor (brilho)
        val_frame = tk.Frame(self.shell, bg=style.bg_color)
        val_frame.pack(fill='x', pady=2)
        tk.Label(val_frame, text="VAL", fg="gray", bg=style.bg_color,
                font=("Arial", 7)).pack(side='left', padx=5)

        self.val_canvas = tk.Canvas(val_frame, height=10, highlightthickness=0, bd=0)
        self.val_canvas.pack(side='left', fill='x', expand=True)

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

        if self.callback:
            self.callback(hex_c)

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

    def get_color(self) -> str:
        """Retorna a cor atual em formato hexadecimal"""
        rgb = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        return '#%02x%02x%02x' % tuple(int(x*255) for x in rgb)


class ModernSlider:
    """Slider moderno com estilo customizável"""

    def __init__(self, container: tk.Frame, text: str, de: int, ate: int,
                 menu_ref: ClivMenu, default: Optional[int] = None,
                 callback: Optional[Callable[[int], None]] = None,
                 style: Optional[WidgetStyle] = None):
        """
        Cria um slider

        Args:
            container: Container pai
            text: Label do slider
            de: Valor mínimo
            ate: Valor máximo
            menu_ref: Referência ao menu
            default: Valor padrão
            callback: Função chamada quando o valor muda
            style: Estilo customizado
        """
        self.de, self.ate = de, ate
        self.theme = menu_ref.theme
        self.callback = callback
        self.current_value = default if default is not None else de

        if style is None:
            style = WidgetStyle()

        bg = menu_ref.bg_color if menu_ref else style.bg_color

        self.shell = tk.Frame(container, bg=bg, pady=style.padding[0], bd=0)

        if style.pack:
            self.shell.pack(fill='x', padx=style.padding[3])
        else:
            self.shell.place(x=style.x, y=style.y, width=style.width, height=style.height)

        f = tk.Frame(self.shell, bg=bg)
        f.pack(fill='x')

        tk.Label(f, text=text, bg=bg, fg="white",
                font=style.font).pack(side='left')

        self.lval = tk.Label(f, text=str(self.current_value), bg=bg,
                            fg=self.theme, font=style.font)
        self.lval.pack(side='right')

        canvas_width = style.width if style.width else 320
        self.canvas = tk.Canvas(self.shell, width=canvas_width, height=20, bg=bg,
                               highlightthickness=0, bd=0)
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.update)
        self.canvas.bind("<Button-1>", self.update)

        initial_pos = 10 + ((self.current_value - self.de) / (self.ate - self.de)) * (canvas_width - 20)
        self.update(None, initial_pos)

    def update(self, event, mx=None):
        """Atualiza o slider"""
        canvas_width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 320
        x = mx if mx is not None else event.x
        x = max(10, min(x, canvas_width - 10))

        self.canvas.delete("all")

        # Track
        self.canvas.create_line(10, 10, canvas_width - 10, 10,
                               fill="#1a1a1a", width=6, capstyle='round')

        # Progress
        self.canvas.create_line(10, 10, x, 10, fill=self.theme,
                               width=6, capstyle='round')

        # Thumb
        self.canvas.create_oval(x-8, 2, x+8, 18, fill="white",
                               outline=self.theme, width=3)

        val = int(self.de + ((x-10)/(canvas_width - 20)) * (self.ate - self.de))
        self.current_value = val
        self.lval.config(text=str(val))

        if self.callback:
            self.callback(val)

    def get_value(self) -> int:
        """Retorna o valor atual"""
        return self.current_value

    def set_value(self, value: int):
        """Define o valor do slider"""
        value = max(self.de, min(value, self.ate))
        canvas_width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 320
        pos = 10 + ((value - self.de) / (self.ate - self.de)) * (canvas_width - 20)
        self.update(None, pos)


class ModernCheck:
    """Checkbox moderno"""

    def __init__(self, container: tk.Frame, text: str, menu_ref: ClivMenu,
                 default: bool = False,
                 callback: Optional[Callable[[bool], None]] = None,
                 style: Optional[WidgetStyle] = None):
        """
        Cria um checkbox

        Args:
            container: Container pai
            text: Label do checkbox
            menu_ref: Referência ao menu
            default: Estado padrão
            callback: Função chamada quando o estado muda
            style: Estilo customizado
        """
        self.marcado = default
        self.theme = menu_ref.theme
        self.callback = callback

        if style is None:
            style = WidgetStyle()

        bg = menu_ref.bg_color if menu_ref else style.bg_color

        self.shell = tk.Frame(container, bg=bg, pady=style.padding[0], bd=0)

        if style.pack:
            self.shell.pack(fill='x', padx=style.padding[3])
        else:
            self.shell.place(x=style.x, y=style.y, width=style.width, height=style.height)

        self.canvas = tk.Canvas(self.shell, width=18, height=18, bg=bg,
                               highlightthickness=0, bd=0, cursor="hand2")
        self.canvas.pack(side='left')

        label = tk.Label(self.shell, text=text, bg=bg, fg="white",
                        font=style.font, cursor="hand2")
        label.pack(side='left', padx=10)

        self.canvas.bind("<Button-1>", lambda e: self.toggle())
        label.bind("<Button-1>", lambda e: self.toggle())

        self.draw()

    def draw(self):
        """Desenha o checkbox"""
        self.canvas.delete("all")

        if self.marcado:
            self.canvas.create_rectangle(1, 1, 17, 17, outline=self.theme,
                                        width=2, fill=self.theme)
            self.canvas.create_line(5, 9, 8, 13, fill="white", width=2, capstyle='round')
            self.canvas.create_line(8, 13, 14, 6, fill="white", width=2, capstyle='round')
        else:
            bg = self.shell.cget('bg')
            self.canvas.create_rectangle(1, 1, 17, 17, outline=self.theme,
                                        width=2, fill=bg)

    def toggle(self):
        """Alterna estado do checkbox"""
        self.marcado = not self.marcado
        self.draw()

        if self.callback:
            self.callback(self.marcado)

    def get_value(self) -> bool:
        """Retorna estado atual"""
        return self.marcado

    def set_value(self, value: bool):
        """Define o estado do checkbox"""
        self.marcado = value
        self.draw()


class KeyBind:
    """Widget para captura de teclas"""

    def __init__(self, container: tk.Frame, text: str, var_name: str,
                 menu_ref: ClivMenu, default: str = "NONE",
                 callback: Optional[Callable[[str], None]] = None,
                 style: Optional[WidgetStyle] = None):
        """
        Cria um capturador de teclas

        Args:
            container: Container pai
            text: Label do widget
            var_name: Nome da variável
            menu_ref: Referência ao menu
            default: Tecla padrão
            callback: Função chamada quando a tecla muda
            style: Estilo customizado
        """
        self.menu = menu_ref
        self.var_name = var_name
        self.key = default
        self.listening = False
        self.callback = callback

        if style is None:
            style = WidgetStyle()

        self.shell = tk.Frame(container, bg=menu_ref.bg_color,
                             pady=style.padding[0], bd=0)

        if style.pack:
            self.shell.pack(fill='x', padx=style.padding[3])
        else:
            self.shell.place(x=style.x, y=style.y, width=style.width, height=style.height)

        tk.Label(self.shell, text=text, bg=menu_ref.bg_color, fg="white",
                font=style.font).pack(side='left')

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

                if self.callback:
                    self.callback(self.key)
        except Exception as e:
            self.btn.config(text="ERRO", fg="red", state='normal')
            self.listening = False

    def get_key(self) -> str:
        """Retorna a tecla atual"""
        return self.key


class ModernButton:
    """Botão moderno com efeitos"""

    def __init__(self, container: tk.Frame, text: str, menu_ref: ClivMenu,
                 callback: Optional[Callable] = None, button_style: str = "primary",
                 style: Optional[WidgetStyle] = None):
        """
        Cria um botão

        Args:
            container: Container pai
            text: Texto do botão
            menu_ref: Referência ao menu
            callback: Função chamada ao clicar
            button_style: Estilo do botão ('primary', 'success', 'danger', 'warning', 'info')
            style: Estilo customizado
        """
        self.menu = menu_ref
        self.callback = callback

        if style is None:
            style = WidgetStyle()

        colors = {
            'primary': menu_ref.theme,
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db'
        }

        color = colors.get(button_style, menu_ref.theme)

        self.shell = tk.Frame(container, bg=menu_ref.bg_color,
                             pady=style.padding[0], bd=0)

        if style.pack:
            self.shell.pack(fill='x', padx=style.padding[3])
        else:
            self.shell.place(x=style.x, y=style.y, width=style.width, height=style.height)

        self.btn = tk.Button(self.shell, text=text.upper(), bg=color, fg="white",
                            font=style.font, bd=0, cursor="hand2",
                            command=self._on_click, activebackground=color,
                            relief='flat')
        self.btn.pack(fill='x', ipady=10)

        self.btn.bind("<Enter>", lambda e: self.btn.config(relief='raised'))
        self.btn.bind("<Leave>", lambda e: self.btn.config(relief='flat'))

    def _on_click(self):
        """Callback do botão"""
        if self.callback:
            self.callback()
