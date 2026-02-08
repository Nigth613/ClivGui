"""
EXEMPLO 1: SYSTEM MONITOR DASHBOARD
Sistema de monitoramento em tempo real com gráficos animados
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from cliv_gui import ClivMenu, ModernGraph, ModernSlider, ModernCheck, ImageSeparator, ModernButton
import threading
import time
import random
import psutil  # pip install psutil


class SystemMonitor:
    def __init__(self):
        # Criar menu principal
        self.menu = ClivMenu(
            title="SYSTEM MONITOR PRO",
            theme_color="#00d4ff",
            part_color="cyan",
            part_count=60,
            part_speed=(0.4, 1.2)
        )

        self.running = True
        self.update_interval = 1000  # 1 segundo

        # Criar abas
        self.setup_dashboard()
        self.setup_settings()

        # Iniciar monitoramento
        self.start_monitoring()

    def setup_dashboard(self):
        """Configura a aba de dashboard"""
        dashboard = self.menu.add_tab("DASHBOARD")

        ImageSeparator(dashboard, "🖥️ SYSTEM METRICS", menu_ref=self.menu)

        # Gráficos de monitoramento
        self.cpu_graph = ModernGraph(dashboard, "CPU USAGE (%)", self.menu)
        self.ram_graph = ModernGraph(dashboard, "RAM USAGE (%)", self.menu)
        self.disk_graph = ModernGraph(dashboard, "DISK I/O (MB/s)", self.menu)

        ImageSeparator(dashboard, "📊 REAL-TIME DATA", menu_ref=self.menu)

        # Botões de controle
        ModernButton(
            dashboard,
            "🔄 Force Update",
            self.menu,
            callback=self.force_update,
            style="info"
        )

        ModernButton(
            dashboard,
            "📸 Capture Snapshot",
            self.menu,
            callback=self.capture_snapshot,
            style="success"
        )

        ModernButton(
            dashboard,
            "🧹 Clear Graphs",
            self.menu,
            callback=self.clear_graphs,
            style="warning"
        )

    def setup_settings(self):
        """Configura a aba de configurações"""
        settings = self.menu.add_tab("SETTINGS")

        ImageSeparator(settings, "⚙️ MONITOR CONFIG", menu_ref=self.menu)

        # Controle de intervalo de atualização
        ModernSlider(
            settings,
            "Update Interval (ms)",
            500, 5000,
            self.menu,
            default=1000,
            callback=self.set_update_interval
        )

        # Opções de monitoramento
        ModernCheck(
            settings,
            "Enable CPU Monitoring",
            self.menu,
            default=True,
            callback=lambda v: self.toggle_monitoring("cpu", v)
        )

        ModernCheck(
            settings,
            "Enable RAM Monitoring",
            self.menu,
            default=True,
            callback=lambda v: self.toggle_monitoring("ram", v)
        )

        ModernCheck(
            settings,
            "Enable Disk Monitoring",
            self.menu,
            default=True,
            callback=lambda v: self.toggle_monitoring("disk", v)
        )

        ModernCheck(
            settings,
            "Show Notifications",
            self.menu,
            default=True,
            callback=lambda v: setattr(self, 'show_notifs', v)
        )

        ImageSeparator(settings, "🎨 APPEARANCE", menu_ref=self.menu)

        ModernSlider(
            settings,
            "Window Opacity",
            30, 100,
            self.menu,
            default=95,
            callback=self.menu.set_alpha
        )

        # Inicializar flags
        self.monitor_cpu = True
        self.monitor_ram = True
        self.monitor_disk = True
        self.show_notifs = True

    def start_monitoring(self):
        """Inicia o loop de monitoramento"""
        def monitor_loop():
            last_disk_io = psutil.disk_io_counters()

            while self.running:
                try:
                    # CPU
                    if self.monitor_cpu:
                        cpu_percent = psutil.cpu_percent(interval=0.1)
                        self.cpu_graph.add_value(cpu_percent)

                        # Alerta de CPU alta
                        if cpu_percent > 80 and self.show_notifs:
                            self.menu.show_notification(
                                "⚠️ CPU Alert",
                                f"CPU usage is high: {cpu_percent:.1f}%",
                                3000,
                                "warning"
                            )

                    # RAM
                    if self.monitor_ram:
                        ram = psutil.virtual_memory()
                        ram_percent = ram.percent
                        self.ram_graph.add_value(ram_percent)

                        # Alerta de RAM alta
                        if ram_percent > 85 and self.show_notifs:
                            self.menu.show_notification(
                                "⚠️ RAM Alert",
                                f"Memory usage is critical: {ram_percent:.1f}%",
                                3000,
                                "error"
                            )

                    # Disk I/O
                    if self.monitor_disk:
                        current_disk_io = psutil.disk_io_counters()
                        read_mb = (current_disk_io.read_bytes - last_disk_io.read_bytes) / 1024 / 1024
                        write_mb = (current_disk_io.write_bytes - last_disk_io.write_bytes) / 1024 / 1024
                        total_io = read_mb + write_mb

                        self.disk_graph.add_value(total_io * 10)  # Escalar para visualização
                        last_disk_io = current_disk_io

                    time.sleep(self.update_interval / 1000)

                except Exception as e:
                    print(f"Erro no monitoramento: {e}")
                    time.sleep(1)

        # Iniciar thread de monitoramento
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()

    def set_update_interval(self, value):
        """Define intervalo de atualização"""
        self.update_interval = value
        self.menu.show_notification(
            "Settings",
            f"Update interval set to {value}ms",
            2000,
            "info"
        )

    def toggle_monitoring(self, metric, enabled):
        """Ativa/desativa monitoramento de uma métrica"""
        if metric == "cpu":
            self.monitor_cpu = enabled
        elif metric == "ram":
            self.monitor_ram = enabled
        elif metric == "disk":
            self.monitor_disk = enabled

        status = "enabled" if enabled else "disabled"
        self.menu.show_notification(
            "Monitor",
            f"{metric.upper()} monitoring {status}",
            2000,
            "info"
        )

    def force_update(self):
        """Força atualização imediata"""
        self.menu.show_notification(
            "Update",
            "Forcing system metrics refresh...",
            2000,
            "info"
        )

    def capture_snapshot(self):
        """Captura snapshot dos dados atuais"""
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        snapshot = f"CPU: {cpu:.1f}% | RAM: {ram:.1f}% | Disk: {disk:.1f}%"

        self.menu.show_notification(
            "📸 Snapshot Captured",
            snapshot,
            5000,
            "success"
        )
        print(f"\n[SNAPSHOT] {snapshot}")

    def clear_graphs(self):
        """Limpa todos os gráficos"""
        self.cpu_graph.values = [0] * 50
        self.ram_graph.values = [0] * 50
        self.disk_graph.values = [0] * 50

        self.cpu_graph.update_graph()
        self.ram_graph.update_graph()
        self.disk_graph.update_graph()

        self.menu.show_notification(
            "Graphs",
            "All graphs cleared",
            2000,
            "success"
        )

    def run(self):
        """Inicia o monitor"""
        self.menu.show_notification(
            "System Monitor",
            "Monitoring started successfully!",
            3000,
            "success"
        )
        self.menu.run("insert")
        self.running = False


if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.run()
