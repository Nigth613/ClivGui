"""
EXEMPLO 3: GAME OVERLAY CONTROLLER
Sistema de overlay para jogos com ESP, aimbot e configurações avançadas
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from cliv_gui import (ClivMenu, ProcessOverlay, ModernSlider, ModernCheck,
                      ImageSeparator, ModernButton, KeyBind, DynamicColorPicker,
                      ModernGraph)
import threading
import time
import random
import tkinter as tk


class GameOverlayController:
    def __init__(self):
        # Criar menu principal
        self.menu = ClivMenu(
            title="🎮 GAME OVERLAY PRO",
            theme_color="#00ff41",
            part_color="#39ff14",
            part_count=80,
            part_speed=(0.5, 1.5),
            enable_tray_icon=True
        )

        # Configurações do overlay
        self.overlay = None
        self.overlay_active = False
        self.target_process = "notepad.exe"  # Processo alvo (exemplo)

        # Configurações ESP
        self.esp_enabled = False
        self.box_esp = True
        self.health_esp = True
        self.distance_esp = True
        self.skeleton_esp = False

        # Configurações Aimbot
        self.aimbot_enabled = False
        self.aimbot_fov = 180
        self.aimbot_smooth = 5
        self.aimbot_target = "head"

        # Criar abas
        self.setup_esp_tab()
        self.setup_aimbot_tab()
        self.setup_visuals_tab()
        self.setup_settings_tab()

        # Iniciar sistema de overlay
        self.start_overlay_system()

    def setup_esp_tab(self):
        """Configura a aba de ESP"""
        esp = self.menu.add_tab("ESP")

        ImageSeparator(esp, "👁️ ESP SETTINGS", menu_ref=self.menu)

        # Toggle principal do ESP
        ModernCheck(
            esp,
            "🔴 Enable ESP System",
            self.menu,
            default=False,
            callback=self.toggle_esp
        )

        ImageSeparator(esp, "📦 BOX ESP", menu_ref=self.menu)

        ModernCheck(
            esp,
            "Show Box ESP",
            self.menu,
            default=True,
            callback=lambda v: setattr(self, 'box_esp', v)
        )

        # Cor do box ESP
        self.box_color_picker = DynamicColorPicker(esp, "Box Color", self.menu)

        ModernSlider(
            esp,
            "Box Thickness",
            1, 5,
            self.menu,
            default=2,
            callback=lambda v: self.update_esp_setting("box_thickness", v)
        )

        ImageSeparator(esp, "💚 HEALTH ESP", menu_ref=self.menu)

        ModernCheck(
            esp,
            "Show Health Bars",
            self.menu,
            default=True,
            callback=lambda v: setattr(self, 'health_esp', v)
        )

        ModernCheck(
            esp,
            "Show Distance",
            self.menu,
            default=True,
            callback=lambda v: setattr(self, 'distance_esp', v)
        )

        ImageSeparator(esp, "🦴 SKELETON ESP", menu_ref=self.menu)

        ModernCheck(
            esp,
            "Show Skeleton",
            self.menu,
            default=False,
            callback=lambda v: setattr(self, 'skeleton_esp', v)
        )

        self.skeleton_color_picker = DynamicColorPicker(esp, "Skeleton Color", self.menu)

        ModernButton(
            esp,
            "🔄 Refresh ESP",
            self.menu,
            callback=self.refresh_esp,
            style="info"
        )

    def setup_aimbot_tab(self):
        """Configura a aba de Aimbot"""
        aimbot = self.menu.add_tab("AIMBOT")

        ImageSeparator(aimbot, "🎯 AIMBOT SETTINGS", menu_ref=self.menu)

        # Toggle principal do aimbot
        ModernCheck(
            aimbot,
            "🔴 Enable Aimbot",
            self.menu,
            default=False,
            callback=self.toggle_aimbot
        )

        ImageSeparator(aimbot, "🎪 FIELD OF VIEW", menu_ref=self.menu)

        ModernSlider(
            aimbot,
            "FOV Radius",
            10, 500,
            self.menu,
            default=180,
            callback=self.set_fov
        )

        # Visualizador do FOV
        self.fov_graph = ModernGraph(aimbot, "FOV VISUALIZATION", self.menu)

        ImageSeparator(aimbot, "🎚️ SMOOTHING", menu_ref=self.menu)

        ModernSlider(
            aimbot,
            "Aim Smoothness",
            1, 20,
            self.menu,
            default=5,
            callback=self.set_smoothness
        )

        ImageSeparator(aimbot, "🎯 TARGET SELECTION", menu_ref=self.menu)

        # Frame para seleção de alvo
        target_frame = tk.Frame(aimbot, bg=self.menu.bg_color, pady=10)
        target_frame.pack(fill='x', padx=30)

        tk.Label(
            target_frame,
            text="Target Bone:",
            bg=self.menu.bg_color,
            fg="white",
            font=("Arial", 8, "bold")
        ).pack(side='left')

        targets = ["Head", "Neck", "Chest", "Pelvis"]
        for target in targets:
            btn = tk.Radiobutton(
                target_frame,
                text=target,
                bg=self.menu.bg_color,
                fg=self.menu.theme,
                selectcolor="#1a1a1a",
                activebackground=self.menu.bg_color,
                activeforeground=self.menu.theme,
                font=("Arial", 7),
                value=target.lower(),
                command=lambda t=target: self.set_target_bone(t.lower())
            )
            btn.pack(side='left', padx=5)
            if target.lower() == "head":
                btn.select()

        ImageSeparator(aimbot, "⌨️ KEYBINDS", menu_ref=self.menu)

        KeyBind(aimbot, "Aimbot Key", "AIMBOT_KEY", self.menu, default="MOUSE5")
        KeyBind(aimbot, "Triggerbot Key", "TRIGGER_KEY", self.menu, default="SHIFT")

        ModernButton(
            aimbot,
            "🧪 Test Aimbot",
            self.menu,
            callback=self.test_aimbot,
            style="warning"
        )

    def setup_visuals_tab(self):
        """Configura a aba de visuais"""
        visuals = self.menu.add_tab("VISUALS")

        ImageSeparator(visuals, "🌟 VISUAL EFFECTS", menu_ref=self.menu)

        ModernCheck(
            visuals,
            "Wallhack (See Through Walls)",
            self.menu,
            default=False,
            callback=lambda v: self.menu.show_notification("Visuals", f"Wallhack: {'ON' if v else 'OFF'}", 2000, "warning")
        )

        ModernCheck(
            visuals,
            "Glow ESP",
            self.menu,
            default=False,
            callback=lambda v: self.menu.show_notification("Visuals", f"Glow ESP: {'ON' if v else 'OFF'}", 2000, "info")
        )

        ModernCheck(
            visuals,
            "Chams (Player Models)",
            self.menu,
            default=False,
            callback=lambda v: self.menu.show_notification("Visuals", f"Chams: {'ON' if v else 'OFF'}", 2000, "info")
        )

        ImageSeparator(visuals, "🎨 COLORS", menu_ref=self.menu)

        self.enemy_color = DynamicColorPicker(visuals, "Enemy Color", self.menu)
        self.ally_color = DynamicColorPicker(visuals, "Ally Color", self.menu)

        ImageSeparator(visuals, "💡 BRIGHTNESS", menu_ref=self.menu)

        ModernSlider(
            visuals,
            "World Brightness",
            0, 200,
            self.menu,
            default=100,
            callback=lambda v: self.menu.show_notification("Visuals", f"Brightness: {v}%", 1500, "info")
        )

        ModernSlider(
            visuals,
            "Night Mode",
            0, 100,
            self.menu,
            default=0,
            callback=lambda v: self.menu.show_notification("Visuals", f"Night Mode: {v}%", 1500, "info")
        )

        ImageSeparator(visuals, "🔦 MISC VISUALS", menu_ref=self.menu)

        ModernCheck(
            visuals,
            "No Flash",
            self.menu,
            default=False
        )

        ModernCheck(
            visuals,
            "No Smoke",
            self.menu,
            default=False
        )

        ModernCheck(
            visuals,
            "Radar Hack",
            self.menu,
            default=False
        )

    def setup_settings_tab(self):
        """Configura a aba de configurações"""
        settings = self.menu.add_tab("SETTINGS")

        ImageSeparator(settings, "⚙️ OVERLAY CONFIG", menu_ref=self.menu)

        # Campo para processo alvo
        process_frame = tk.Frame(settings, bg=self.menu.bg_color, pady=10)
        process_frame.pack(fill='x', padx=30)

        tk.Label(
            process_frame,
            text="Target Process:",
            bg=self.menu.bg_color,
            fg="white",
            font=("Arial", 8, "bold")
        ).pack(anchor='w')

        self.process_entry = tk.Entry(
            process_frame,
            bg="#1a1a1a",
            fg=self.menu.theme,
            font=("Arial", 9),
            bd=2,
            relief='solid',
            insertbackground=self.menu.theme
        )
        self.process_entry.pack(fill='x', pady=5)
        self.process_entry.insert(0, self.target_process)

        ModernButton(
            settings,
            "🔄 Update Process",
            self.menu,
            callback=self.update_target_process,
            style="info"
        )

        ImageSeparator(settings, "🎨 MENU SETTINGS", menu_ref=self.menu)

        ModernSlider(
            settings,
            "Menu Opacity",
            20, 100,
            self.menu,
            default=95,
            callback=self.menu.set_alpha
        )

        ImageSeparator(settings, "💾 CONFIG MANAGEMENT", menu_ref=self.menu)

        ModernButton(
            settings,
            "💾 Save Config",
            self.menu,
            callback=self.save_config,
            style="success"
        )

        ModernButton(
            settings,
            "📂 Load Config",
            self.menu,
            callback=self.load_config,
            style="info"
        )

        ModernButton(
            settings,
            "🔄 Reset to Default",
            self.menu,
            callback=self.reset_config,
            style="danger"
        )

        ImageSeparator(settings, "ℹ️ STATUS", menu_ref=self.menu)

        # Status do overlay
        status_frame = tk.Frame(settings, bg=self.menu.bg_color, pady=10)
        status_frame.pack(fill='x', padx=30)

        self.status_label = tk.Label(
            status_frame,
            text="● Overlay: Inactive",
            bg=self.menu.bg_color,
            fg="red",
            font=("Arial", 9, "bold")
        )
        self.status_label.pack(anchor='w')

    def start_overlay_system(self):
        """Inicia o sistema de overlay em background"""
        def overlay_monitor():
            while True:
                try:
                    if self.overlay_active and self.esp_enabled:
                        # Atualizar visualizações (simulado)
                        pass
                    time.sleep(0.1)
                except:
                    time.sleep(1)

        thread = threading.Thread(target=overlay_monitor, daemon=True)
        thread.start()

    def toggle_esp(self, enabled):
        """Ativa/desativa ESP"""
        self.esp_enabled = enabled

        if enabled:
            self.activate_overlay()
            self.menu.show_notification(
                "ESP System",
                "ESP activated successfully!",
                3000,
                "success"
            )
        else:
            self.deactivate_overlay()
            self.menu.show_notification(
                "ESP System",
                "ESP deactivated",
                2000,
                "info"
            )

    def toggle_aimbot(self, enabled):
        """Ativa/desativa Aimbot"""
        self.aimbot_enabled = enabled

        if enabled:
            self.menu.show_notification(
                "Aimbot",
                f"Aimbot activated! FOV: {self.aimbot_fov}px",
                3000,
                "warning"
            )
        else:
            self.menu.show_notification(
                "Aimbot",
                "Aimbot deactivated",
                2000,
                "info"
            )

    def activate_overlay(self):
        """Ativa o overlay no processo alvo"""
        try:
            # Criar overlay (exemplo com notepad)
            self.overlay_active = True
            self.status_label.config(text="● Overlay: Active", fg="lime")

            self.menu.show_notification(
                "Overlay",
                f"Attached to {self.target_process}",
                3000,
                "success"
            )
        except Exception as e:
            self.menu.show_notification(
                "Error",
                f"Failed to attach overlay: {str(e)}",
                3000,
                "error"
            )

    def deactivate_overlay(self):
        """Desativa o overlay"""
        self.overlay_active = False
        self.status_label.config(text="● Overlay: Inactive", fg="red")

    def set_fov(self, value):
        """Define FOV do aimbot"""
        self.aimbot_fov = value
        # Atualizar gráfico visual
        self.fov_graph.add_value(value / 5)  # Escalar para visualização

    def set_smoothness(self, value):
        """Define suavidade do aimbot"""
        self.aimbot_smooth = value
        self.menu.show_notification("Aimbot", f"Smoothness: {value}", 1500, "info")

    def set_target_bone(self, bone):
        """Define osso alvo do aimbot"""
        self.aimbot_target = bone
        self.menu.show_notification("Aimbot", f"Target: {bone.upper()}", 2000, "info")

    def update_esp_setting(self, setting, value):
        """Atualiza configuração ESP"""
        self.menu.show_notification("ESP", f"{setting}: {value}", 1500, "info")

    def refresh_esp(self):
        """Recarrega ESP"""
        self.menu.show_notification(
            "ESP",
            "ESP refreshed successfully!",
            2000,
            "success"
        )

    def test_aimbot(self):
        """Testa o aimbot"""
        self.menu.show_notification(
            "Test",
            "Aimbot test initiated...",
            2000,
            "warning"
        )

        # Simular teste
        self.menu.root.after(2000, lambda: self.menu.show_notification(
            "Test Complete",
            "Aimbot is functioning correctly!",
            3000,
            "success"
        ))

    def update_target_process(self):
        """Atualiza processo alvo"""
        new_process = self.process_entry.get().strip()
        if new_process:
            self.target_process = new_process
            self.menu.show_notification(
                "Process",
                f"Target updated to: {new_process}",
                3000,
                "info"
            )

    def save_config(self):
        """Salva configuração atual"""
        self.menu.show_notification(
            "Config",
            "Configuration saved successfully!",
            3000,
            "success"
        )

    def load_config(self):
        """Carrega configuração"""
        self.menu.show_notification(
            "Config",
            "Configuration loaded!",
            2000,
            "info"
        )

    def reset_config(self):
        """Reseta para configuração padrão"""
        self.menu.show_notification(
            "Config",
            "Reset to default settings",
            2000,
            "warning"
        )

    def run(self):
        """Inicia o controller"""
        self.menu.show_notification(
            "Game Overlay",
            "Controller started! Configure your settings.",
            4000,
            "success"
        )
        self.menu.run("insert")


if __name__ == "__main__":
    controller = GameOverlayController()
    controller.run()
