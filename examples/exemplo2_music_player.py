"""
EXEMPLO 2: ADVANCED MUSIC PLAYER
Player de música com playlist, equalizer visual e controles completos
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from cliv_gui import ClivMenu, AudioPlayer, ModernSlider, ModernCheck, ImageSeparator, ModernButton, ModernGraph
import threading
import time
import random
from tkinter import filedialog
import tkinter as tk


class MusicPlayer:
    def __init__(self):
        # Criar menu principal
        self.menu = ClivMenu(
            title="🎵 MUSIC PLAYER ULTRA",
            theme_color="#e91e63",
            part_color="#ff69b4",
            part_count=70,
            part_speed=(0.3, 1.5)
        )

        self.playlist = []
        self.current_track_index = 0
        self.visualizer_enabled = True
        self.bass_boost = 0
        self.treble = 0

        # Criar abas
        self.setup_player_tab()
        self.setup_playlist_tab()
        self.setup_equalizer_tab()

        # Iniciar visualizador
        self.start_visualizer()

    def setup_player_tab(self):
        """Configura a aba do player principal"""
        player = self.menu.add_tab("PLAYER")

        ImageSeparator(player, "🎧 AUDIO PLAYER", menu_ref=self.menu)

        # Player de áudio integrado
        self.audio_player = AudioPlayer(
            player,
            self.menu,
            audio_path="music.mp3",  # Arquivo padrão (pode não existir)
            autoplay=False,
            loop=False
        )

        ImageSeparator(player, "🎼 TRACK INFO", menu_ref=self.menu)

        # Informações da faixa
        info_frame = tk.Frame(player, bg=self.menu.bg_color, pady=10)
        info_frame.pack(fill='x', padx=30)

        self.track_label = tk.Label(
            info_frame,
            text="No track loaded",
            bg=self.menu.bg_color,
            fg=self.menu.theme,
            font=("Arial", 10, "bold")
        )
        self.track_label.pack()

        self.status_label = tk.Label(
            info_frame,
            text="Ready to play",
            bg=self.menu.bg_color,
            fg="gray",
            font=("Arial", 8)
        )
        self.status_label.pack()

        ImageSeparator(player, "🎚️ CONTROLS", menu_ref=self.menu)

        # Botões de controle de playlist
        ModernButton(
            player,
            "⏮️ Previous Track",
            self.menu,
            callback=self.previous_track,
            style="info"
        )

        ModernButton(
            player,
            "⏭️ Next Track",
            self.menu,
            callback=self.next_track,
            style="info"
        )

        ModernButton(
            player,
            "📂 Load Audio File",
            self.menu,
            callback=self.load_audio_file,
            style="success"
        )

        ModernButton(
            player,
            "🔀 Shuffle Playlist",
            self.menu,
            callback=self.shuffle_playlist,
            style="warning"
        )

    def setup_playlist_tab(self):
        """Configura a aba de playlist"""
        playlist = self.menu.add_tab("PLAYLIST")

        ImageSeparator(playlist, "📋 PLAYLIST MANAGER", menu_ref=self.menu)

        # Lista de músicas (simulada)
        list_frame = tk.Frame(playlist, bg=self.menu.bg_color, pady=10)
        list_frame.pack(fill='both', expand=True, padx=30)

        self.playlist_text = tk.Text(
            list_frame,
            bg="#0a0a15",
            fg="white",
            font=("Courier", 9),
            height=15,
            bd=0,
            highlightthickness=2,
            highlightbackground=self.menu.theme
        )
        self.playlist_text.pack(fill='both', expand=True)
        self.update_playlist_display()

        ImageSeparator(playlist, "➕ PLAYLIST ACTIONS", menu_ref=self.menu)

        ModernButton(
            playlist,
            "➕ Add Folder",
            self.menu,
            callback=self.add_folder,
            style="success"
        )

        ModernButton(
            playlist,
            "🗑️ Clear Playlist",
            self.menu,
            callback=self.clear_playlist,
            style="danger"
        )

        ModernButton(
            playlist,
            "💾 Save Playlist",
            self.menu,
            callback=self.save_playlist,
            style="info"
        )

    def setup_equalizer_tab(self):
        """Configura a aba do equalizador"""
        eq = self.menu.add_tab("EQUALIZER")

        ImageSeparator(eq, "🎛️ AUDIO EQUALIZER", menu_ref=self.menu)

        # Visualizador de áudio
        self.visualizer = ModernGraph(eq, "AUDIO SPECTRUM", self.menu)

        ImageSeparator(eq, "🎚️ EQ CONTROLS", menu_ref=self.menu)

        # Controles de equalização
        ModernSlider(
            eq,
            "🔊 Master Volume",
            0, 100,
            self.menu,
            default=50,
            callback=self.set_master_volume
        )

        ModernSlider(
            eq,
            "🔉 Bass Boost",
            -10, 10,
            self.menu,
            default=0,
            callback=self.set_bass
        )

        ModernSlider(
            eq,
            "🔈 Treble",
            -10, 10,
            self.menu,
            default=0,
            callback=self.set_treble
        )

        ModernSlider(
            eq,
            "🎵 Mid Range",
            -10, 10,
            self.menu,
            default=0,
            callback=self.set_midrange
        )

        ImageSeparator(eq, "✨ EFFECTS", menu_ref=self.menu)

        ModernCheck(
            eq,
            "Enable Visualizer",
            self.menu,
            default=True,
            callback=self.toggle_visualizer
        )

        ModernCheck(
            eq,
            "Bass Boost Enhancement",
            self.menu,
            default=False,
            callback=lambda v: self.menu.show_notification("EQ", f"Bass Enhancement: {'ON' if v else 'OFF'}", 2000, "info")
        )

        ModernCheck(
            eq,
            "3D Surround Sound",
            self.menu,
            default=False,
            callback=lambda v: self.menu.show_notification("EQ", f"3D Sound: {'ON' if v else 'OFF'}", 2000, "info")
        )

    def start_visualizer(self):
        """Inicia o visualizador de áudio"""
        def visualizer_loop():
            while True:
                try:
                    if self.visualizer_enabled and self.audio_player.playing:
                        # Simular dados de espectro de áudio
                        value = random.randint(30, 100)
                        self.visualizer.add_value(value)
                    time.sleep(0.05)  # 20 FPS
                except:
                    time.sleep(0.1)

        thread = threading.Thread(target=visualizer_loop, daemon=True)
        thread.start()

    def load_audio_file(self):
        """Carrega um arquivo de áudio"""
        try:
            filename = filedialog.askopenfilename(
                title="Select Audio File",
                filetypes=[
                    ("Audio Files", "*.mp3 *.wav *.ogg *.flac"),
                    ("All Files", "*.*")
                ]
            )

            if filename:
                self.audio_player.set_audio_file(filename)
                self.track_label.config(text=os.path.basename(filename))
                self.status_label.config(text="Ready to play")

                # Adicionar à playlist se não estiver
                if filename not in self.playlist:
                    self.playlist.append(filename)
                    self.update_playlist_display()

                self.menu.show_notification(
                    "Track Loaded",
                    f"Loaded: {os.path.basename(filename)}",
                    3000,
                    "success"
                )
        except Exception as e:
            self.menu.show_notification(
                "Error",
                f"Failed to load file: {str(e)}",
                3000,
                "error"
            )

    def add_folder(self):
        """Adiciona todos os arquivos de áudio de uma pasta"""
        try:
            folder = filedialog.askdirectory(title="Select Music Folder")

            if folder:
                count = 0
                for file in os.listdir(folder):
                    if file.endswith(('.mp3', '.wav', '.ogg', '.flac')):
                        full_path = os.path.join(folder, file)
                        if full_path not in self.playlist:
                            self.playlist.append(full_path)
                            count += 1

                self.update_playlist_display()

                self.menu.show_notification(
                    "Playlist",
                    f"Added {count} tracks to playlist",
                    3000,
                    "success"
                )
        except Exception as e:
            self.menu.show_notification(
                "Error",
                f"Failed to add folder: {str(e)}",
                3000,
                "error"
            )

    def update_playlist_display(self):
        """Atualiza a exibição da playlist"""
        self.playlist_text.delete(1.0, tk.END)

        if not self.playlist:
            self.playlist_text.insert(1.0, "Playlist is empty.\nAdd some tracks to get started!")
        else:
            for i, track in enumerate(self.playlist, 1):
                marker = "▶" if i == self.current_track_index + 1 else " "
                track_name = os.path.basename(track)
                self.playlist_text.insert(tk.END, f"{marker} {i:02d}. {track_name}\n")

    def previous_track(self):
        """Toca a faixa anterior"""
        if not self.playlist:
            self.menu.show_notification("Playlist", "Playlist is empty!", 2000, "warning")
            return

        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.play_current_track()

    def next_track(self):
        """Toca a próxima faixa"""
        if not self.playlist:
            self.menu.show_notification("Playlist", "Playlist is empty!", 2000, "warning")
            return

        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.play_current_track()

    def play_current_track(self):
        """Toca a faixa atual da playlist"""
        if self.playlist:
            track = self.playlist[self.current_track_index]
            self.audio_player.set_audio_file(track)
            self.audio_player.play_music()

            self.track_label.config(text=os.path.basename(track))
            self.status_label.config(text=f"Playing ({self.current_track_index + 1}/{len(self.playlist)})")
            self.update_playlist_display()

    def shuffle_playlist(self):
        """Embaralha a playlist"""
        if self.playlist:
            random.shuffle(self.playlist)
            self.current_track_index = 0
            self.update_playlist_display()

            self.menu.show_notification(
                "Playlist",
                "Playlist shuffled!",
                2000,
                "success"
            )
        else:
            self.menu.show_notification(
                "Playlist",
                "Playlist is empty!",
                2000,
                "warning"
            )

    def clear_playlist(self):
        """Limpa a playlist"""
        self.playlist.clear()
        self.current_track_index = 0
        self.update_playlist_display()

        self.menu.show_notification(
            "Playlist",
            "Playlist cleared",
            2000,
            "info"
        )

    def save_playlist(self):
        """Salva a playlist (simulado)"""
        self.menu.show_notification(
            "Save",
            f"Playlist saved ({len(self.playlist)} tracks)",
            3000,
            "success"
        )

    def set_master_volume(self, value):
        """Define volume mestre"""
        volume = value / 100
        # Aplicar ao player (já está implementado internamente)

    def set_bass(self, value):
        """Define reforço de graves"""
        self.bass_boost = value
        self.menu.show_notification("EQ", f"Bass: {value:+d}", 1500, "info")

    def set_treble(self, value):
        """Define agudos"""
        self.treble = value
        self.menu.show_notification("EQ", f"Treble: {value:+d}", 1500, "info")

    def set_midrange(self, value):
        """Define médios"""
        self.menu.show_notification("EQ", f"Mid: {value:+d}", 1500, "info")

    def toggle_visualizer(self, enabled):
        """Ativa/desativa visualizador"""
        self.visualizer_enabled = enabled
        status = "enabled" if enabled else "disabled"
        self.menu.show_notification("Visualizer", f"Visualizer {status}", 2000, "info")

    def run(self):
        """Inicia o player"""
        self.menu.show_notification(
            "Music Player",
            "Welcome! Load your music and enjoy! 🎵",
            4000,
            "success"
        )
        self.menu.run("insert")


if __name__ == "__main__":
    player = MusicPlayer()
    player.run()
