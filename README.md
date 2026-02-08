# CLIV EXTREME 🎮

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

**CLIV EXTREME** é uma biblioteca Python avançada para criação de menus GUI modernos e overlays transparentes sobre processos do Windows. Perfeita para desenvolvimento de ferramentas de produtividade, utilitários de jogos, dashboards customizados e muito mais.

![CLIV EXTREME Banner](https://via.placeholder.com/800x200/8e44ad/ffffff?text=CLIV+EXTREME)

## ✨ Características Principais

### 🎨 Menu Moderno e Personalizável
- Interface GUI sem bordas (borderless) com tema customizável
- Sistema de abas com scroll customizado
- Partículas animadas no fundo
- Transparência ajustável
- Drag & drop para mover a janela
- Imagem de fundo opcional

### 📢 Sistema de Notificações
- Notificações estilo Roblox/Discord
- 4 tipos: `info`, `success`, `warning`, `error`
- Animações suaves de entrada/saída
- Barra de progresso automática
- Empilhamento inteligente de notificações
- Totalmente thread-safe

### 🎯 Process Overlay
- Overlay transparente sobre qualquer processo Windows
- Auto-tracking da janela do processo
- Ferramentas de desenho integradas:
  - Retângulos, círculos, linhas
  - Texto customizável
  - Crosshairs (miras)
  - Transparência ajustável
- Atualização em tempo real (~60 FPS)
- Perfeito para ESPs, overlays de jogos, etc.

### 🎵 Componentes Prontos
- **AudioPlayer**: Player de áudio com controles completos
- **ColorPicker**: Seletor de cores HSV com preview
- **ModernSlider**: Slider customizado
- **ModernCheck**: Checkbox estilizado
- **ModernButton**: Botões com efeitos hover
- **KeyBind**: Captura de teclas
- **ModernGraph**: Gráficos em tempo real
- **MessageBox**: Diálogos customizados

### 🔧 System Tray Integration
- Ícone na bandeja do sistema (opcional)
- Menu de contexto customizável
- Suporte para ícones personalizados

## 📦 Instalação

### Método 1: Via pip (recomendado)
```bash
pip install cliv-extreme
```

### Método 2: Instalação manual
```bash
git clone https://github.com/clivteam/cliv-extreme.git
cd cliv-extreme
pip install -r requirements.txt
python setup.py install
```

### Dependências
```
Pillow>=9.0.0
pygame>=2.0.0
keyboard>=0.13.5
pywin32>=304
psutil>=5.9.0
pystray>=0.19.4
```

## 🚀 Início Rápido

### Menu Básico

```python
from cliv_extreme_fixed import ClivMenu, ModernButton, ModernCheck

# Criar menu
menu = ClivMenu(
    title="MEU APLICATIVO",
    theme_color="#e74c3c",  # Vermelho
    part_color="white",
    part_count=30
)

# Adicionar aba
main_tab = menu.add_tab("PRINCIPAL")

# Adicionar componentes
ModernCheck(main_tab, "Ativar Feature", menu, default=True,
            callback=lambda v: menu.show_notification(
                "Status",
                f"Feature: {'ON' if v else 'OFF'}",
                2000,
                "success"
            ))

ModernButton(main_tab, "Clique Aqui", menu,
             callback=lambda: print("Botão clicado!"),
             style="success")

# Iniciar (hotkey: INSERT)
menu.run("insert")
```

### Process Overlay (ESP/Aimbot Visual)

```python
from cliv_extreme_fixed import ProcessOverlay

# Criar overlay para um jogo
overlay = ProcessOverlay("game.exe", alpha=0.4)

# Desenhar ESP box
overlay.draw_rectangle(100, 100, 200, 300, color="red", thickness=2)

# Desenhar nome do jogador
overlay.draw_text(200, 80, "ENEMY", color="red", font=("Arial", 12, "bold"))

# Desenhar mira
overlay.draw_crosshair(960, 540, size=20, color="lime", thickness=2)

# Desenhar distância
overlay.draw_circle(500, 400, 50, color="yellow", thickness=1)

# Iniciar overlay
overlay.run()
```

### Sistema de Notificações

```python
# Notificação de sucesso
menu.show_notification(
    "Operação Completa",
    "Arquivo salvo com sucesso!",
    duration=3000,
    notif_type="success"
)

# Notificação de erro
menu.show_notification(
    "Erro",
    "Não foi possível conectar ao servidor",
    duration=5000,
    notif_type="error"
)

# Notificação de aviso
menu.show_notification(
    "Atenção",
    "Seu trial expira em 3 dias",
    duration=4000,
    notif_type="warning"
)
```

### Audio Player

```python
from cliv_extreme_fixed import AudioPlayer

# Adicionar player na aba
audio = AudioPlayer(
    container=misc_tab,
    menu_ref=menu,
    audio_path="music.mp3",
    autoplay=True,
    loop=True
)

# Controlar programaticamente
audio.set_volume(0.7)  # 70% volume
audio.play_music()
audio.pause_music()
audio.stop_music()
```

### Color Picker

```python
from cliv_extreme_fixed import DynamicColorPicker

# Criar color picker
color_picker = DynamicColorPicker(
    container=visuals_tab,
    var_name="ESP_COLOR",
    menu_ref=menu
)

# Obter cor selecionada
selected_color = menu.data["ESP_COLOR"]  # Retorna hex: "#ff0000"
```

## 📖 Documentação Completa

### ClivMenu

**Parâmetros:**
- `title` (str): Título da janela
- `theme_color` (str): Cor do tema em hex (ex: "#8e44ad")
- `bg_img_path` (str): Caminho para imagem de fundo (opcional)
- `part_color` (str): Cor das partículas
- `part_count` (int): Quantidade de partículas (padrão: 40)
- `part_speed` (tuple): Range de velocidade (min, max)
- `enable_tray_icon` (bool): Habilitar ícone na bandeja
- `tray_icon_path` (str): Caminho para ícone customizado

**Métodos:**
```python
menu.add_tab(name)                          # Adiciona nova aba
menu.show_tab(name)                         # Mostra aba específica
menu.show_notification(title, msg, dur, tp) # Mostra notificação
menu.show_message(title, msg, type)         # Mostra messagebox
menu.set_alpha(value)                       # Define transparência (0-100)
menu.toggle_visibility()                    # Mostra/oculta menu
menu.run(hotkey)                            # Inicia loop principal
```

### ProcessOverlay

**Parâmetros:**
- `process_name` (str): Nome do processo (ex: "notepad.exe")
- `bg_color` (str): Cor de fundo (padrão: "#000000")
- `alpha` (float): Transparência inicial (0.0 a 1.0)

**Métodos:**
```python
overlay.draw_rectangle(x, y, w, h, color, thickness, fill)
overlay.draw_line(x1, y1, x2, y2, color, thickness)
overlay.draw_circle(x, y, radius, color, thickness, fill)
overlay.draw_text(x, y, text, color, font)
overlay.draw_crosshair(x, y, size, color, thickness)
overlay.clear_drawings()              # Limpa todos os desenhos
overlay.delete_drawing(drawing_id)    # Remove desenho específico
overlay.set_alpha(alpha)              # Ajusta transparência
overlay.start()                       # Inicia overlay
overlay.stop()                        # Para overlay
overlay.run()                         # Inicia loop principal
```

### Componentes

#### ModernSlider
```python
slider = ModernSlider(
    container=tab,
    text="FOV",
    de=1,
    ate=500,
    menu_ref=menu,
    default=120,
    callback=lambda val: print(f"FOV: {val}")
)
value = slider.get_value()
```

#### ModernCheck
```python
checkbox = ModernCheck(
    container=tab,
    text="Enable Wallhack",
    menu_ref=menu,
    default=False,
    callback=lambda checked: print(f"Wallhack: {checked}")
)
is_checked = checkbox.get_value()
```

#### ModernButton
```python
button = ModernButton(
    container=tab,
    text="Execute",
    menu_ref=menu,
    callback=lambda: print("Executed!"),
    style="success"  # primary, success, danger, warning, info
)
```

#### KeyBind
```python
keybind = KeyBind(
    container=tab,
    text="Aimbot Key",
    var_name="AIM_KEY",
    menu_ref=menu,
    default="MOUSE5"
)
key = menu.data["AIM_KEY"]  # Acessa tecla configurada
```

## 🎮 Exemplos de Uso

### 1. Menu de Configurações de Jogo
```python
menu = ClivMenu(title="GAME CONFIG", theme_color="#2ecc71")

settings = menu.add_tab("SETTINGS")

# FOV Slider
ModernSlider(settings, "Field of View", 60, 120, menu, default=90)

# Graphics Quality
ModernCheck(settings, "High Quality Textures", menu, default=True)
ModernCheck(settings, "Enable Shadows", menu, default=True)
ModernCheck(settings, "V-Sync", menu, default=False)

menu.run()
```

### 2. ESP Overlay Completo
```python
import threading
import time

overlay = ProcessOverlay("csgo.exe", alpha=0.3)

def draw_esp():
    while True:
        overlay.clear_drawings()

        # Simular players detectados
        players = [(100, 200), (300, 150), (500, 400)]

        for x, y in players:
            # Box ESP
            overlay.draw_rectangle(x, y, 60, 120, "red", 2)
            # Nome
            overlay.draw_text(x+30, y-20, "ENEMY", "red", ("Arial", 10, "bold"))
            # Health bar
            overlay.draw_rectangle(x-5, y, 3, 120, "lime", 1, fill="lime")

        time.sleep(0.016)  # ~60 FPS

threading.Thread(target=draw_esp, daemon=True).start()
overlay.run()
```

### 3. Dashboard de Sistema
```python
from cliv_extreme_fixed import ModernGraph

menu = ClivMenu(title="SYSTEM MONITOR", theme_color="#3498db")
monitor = menu.add_tab("MONITOR")

# Gráfico de CPU
cpu_graph = ModernGraph(monitor, "CPU USAGE %", menu)

# Gráfico de RAM
ram_graph = ModernGraph(monitor, "RAM USAGE %", menu)

def update_stats():
    import psutil
    cpu_graph.add_value(psutil.cpu_percent())
    ram_graph.add_value(psutil.virtual_memory().percent)
    menu.root.after(1000, update_stats)

menu.root.after(1000, update_stats)
menu.run()
```

## ⚙️ Configuração Avançada

### Tema Customizado
```python
menu = ClivMenu(
    title="CUSTOM THEME",
    theme_color="#e91e63",      # Pink
    bg_img_path="bg.jpg",       # Imagem de fundo
    part_color="#ffffff",       # Partículas brancas
    part_count=100,             # Mais partículas
    part_speed=(0.5, 1.5),      # Velocidade variável
    enable_tray_icon=True,      # Ícone na bandeja
    tray_icon_path="icon.ico"   # Ícone customizado
)
```

### Hotkeys Customizadas
```python
# Usar tecla diferente para abrir/fechar
menu.run(hotkey="f1")  # F1 ao invés de INSERT

# Múltiplas hotkeys
import keyboard
keyboard.add_hotkey("ctrl+shift+m", menu.toggle_visibility)
```

## 🐛 Troubleshooting

### Erro: "pygame.error: No available video device"
```bash
# Instalar dependências de vídeo
pip install --upgrade pygame
```

### Erro: "ImportError: No module named 'win32gui'"
```bash
# Instalar pywin32
pip install pywin32
```

### Overlay não aparece
- Verifique se o processo está rodando
- Execute o script como administrador
- Confirme que o nome do processo está correto (use Task Manager)

### Notificações não aparecem
- Verifique se outras janelas não estão cobrindo
- Ajuste a posição das notificações no código se necessário
- Certifique-se que `show_notification()` está sendo chamado na thread principal

## 📝 Changelog

### v1.0.0 (2024-02-07)
- ✨ Release inicial
- 🎨 Sistema de menu completo
- 🎯 Process Overlay funcional
- 📢 Sistema de notificações
- 🎵 Componentes de UI prontos
- 🔧 System tray integration

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **CLIV Team** - *Trabalho inicial* - [GitHub](https://github.com/clivteam)

## 🙏 Agradecimentos

- Inspirado em menus de jogos modernos
- Comunidade Python pela excelente documentação

## 📞 Suporte

- 📧 Email: clivguicontact@gmail.com

---

⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!

**Made with ❤️ by CLIV Team**
