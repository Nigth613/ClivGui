# 📖 ClivGui - Documentação Completa

**Versão:** 1.0.0
**Última Atualização:** 07/02/2024
**Autor:** Night613
**Licença:** MIT

---

## 📑 Índice

1. [Introdução](#1-introdução)
2. [Instalação](#2-instalação)
3. [Conceitos Básicos](#3-conceitos-básicos)
4. [API Reference](#4-api-reference)
   - [ClivMenu](#41-clivmenu)
   - [ProcessOverlay](#42-processoverlay)
   - [NotificationManager](#43-notificationmanager)
   - [MessageBox](#44-messagebox)
   - [Componentes UI](#45-componentes-ui)
5. [Guias Práticos](#5-guias-práticos)
6. [Exemplos Avançados](#6-exemplos-avançados)
7. [Troubleshooting](#7-troubleshooting)
8. [Best Practices](#8-best-practices)
9. [FAQ](#9-faq)

---

## 1. Introdução

### 1.1 O que é ClivGui?

**ClivGui** é um framework Python completo para criação de interfaces gráficas modernas e overlays transparentes sobre processos Windows. Projetado para desenvolvedores que precisam criar:

- 🎮 Ferramentas para jogos (ESP, aimbots, trainers)
- 🛠️ Utilitários do sistema
- 📊 Dashboards em tempo real
- 🎨 Aplicações com UI moderna
- 🔧 Ferramentas de automação

### 1.2 Principais Características

| Característica | Descrição |
|---------------|-----------|
| **Zero Config** | Funciona imediatamente sem configuração |
| **Modern UI** | Interface inspirada em Roblox/Discord |
| **Process Overlay** | Desenhe sobre qualquer janela Windows |
| **Notifications** | Sistema de notificações toast animadas |
| **Audio Player** | Player de áudio integrado |
| **Color Picker** | Seletor HSV completo |
| **System Tray** | Integração com bandeja do sistema |
| **Thread-Safe** | Seguro para uso com múltiplas threads |

### 1.3 Requisitos do Sistema

- **Sistema Operacional:** Windows 7/8/10/11
- **Python:** 3.7 ou superior
- **Dependências:** Instaladas automaticamente via pip

---

## 2. Instalação

### 2.1 Instalação via pip

```bash
pip install cliv-gui
```

### 2.2 Instalação a partir do código-fonte

```bash
# Clonar repositório
git clone https://github.com/Night613/cliv-gui.git
cd cliv-gui

# Instalar dependências
pip install -r requirements.txt

# Instalar o pacote
python setup.py install
```

### 2.3 Dependências

O ClivGui requer as seguintes bibliotecas (instaladas automaticamente):

```
Pillow>=9.0.0       # Manipulação de imagens
pygame>=2.0.0       # Sistema de áudio
keyboard>=0.13.5    # Captura de teclas
pywin32>=304        # APIs do Windows
psutil>=5.9.0       # Gerenciamento de processos
pystray>=0.19.4     # Ícone na bandeja do sistema
```

### 2.4 Verificar Instalação

```python
import cliv_gui
print(cliv_gui.__version__)  # Deve mostrar: 1.0.0
```

---

## 3. Conceitos Básicos

### 3.1 Estrutura de um Projeto ClivGui

Um projeto ClivGui típico segue esta estrutura:

```python
from cliv_gui import ClivMenu, ModernButton

# 1. Criar menu principal
menu = ClivMenu(title="MEU APP", theme_color="#8e44ad")

# 2. Adicionar abas
tab = menu.add_tab("PRINCIPAL")

# 3. Adicionar componentes
ModernButton(tab, "Clique Aqui", menu,
             callback=lambda: print("Clicado!"))

# 4. Iniciar aplicação
menu.run()
```

### 3.2 Fluxo de Trabalho

```
┌─────────────────┐
│  Criar ClivMenu │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Adicionar Abas │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Adicionar Componentes│
└────────┬────────────┘
         │
         ▼
┌─────────────────┐
│   menu.run()    │
└─────────────────┘
```

### 3.3 Sistema de Abas

Cada menu pode ter múltiplas abas para organizar funcionalidades:

```python
# Criar abas
main_tab = menu.add_tab("PRINCIPAL")
settings_tab = menu.add_tab("CONFIGURAÇÕES")
about_tab = menu.add_tab("SOBRE")

# Adicionar componentes em cada aba
ModernButton(main_tab, "Executar", menu)
ModernSlider(settings_tab, "Volume", 0, 100, menu)
```

---

## 4. API Reference

### 4.1 ClivMenu

Classe principal para criação de menus GUI.

#### Construtor

```python
ClivMenu(
    title="CLIV1 EXTREME",
    theme_color="#8e44ad",
    bg_img_path=None,
    part_color="white",
    part_count=40,
    part_speed=(0.2, 0.8),
    enable_tray_icon=False,
    tray_icon_path=None
)
```

#### Parâmetros

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| `title` | str | "CLIV1 EXTREME" | Título da janela |
| `theme_color` | str | "#8e44ad" | Cor do tema em hexadecimal |
| `bg_img_path` | str | None | Caminho para imagem de fundo |
| `part_color` | str | "white" | Cor das partículas animadas |
| `part_count` | int | 40 | Quantidade de partículas |
| `part_speed` | tuple | (0.2, 0.8) | Velocidade mín/máx das partículas |
| `enable_tray_icon` | bool | False | Habilitar ícone na bandeja |
| `tray_icon_path` | str | None | Caminho do ícone customizado |

#### Métodos Principais

##### add_tab(name: str) -> Frame

Adiciona uma nova aba ao menu.

```python
tab = menu.add_tab("CONFIGURAÇÕES")
```

**Retorna:** Frame do Tkinter onde componentes podem ser adicionados

##### show_tab(name: str)

Exibe uma aba específica.

```python
menu.show_tab("CONFIGURAÇÕES")
```

##### show_notification(title: str, message: str, duration: int = 3000, notif_type: str = "info")

Exibe uma notificação toast.

```python
menu.show_notification(
    "Sucesso",
    "Operação concluída!",
    3000,
    "success"
)
```

**Tipos disponíveis:** `"info"`, `"success"`, `"warning"`, `"error"`

##### show_message(title: str, message: str, msg_type: str = "info")

Exibe um messagebox modal.

```python
menu.show_message(
    "Atenção",
    "Tem certeza que deseja continuar?",
    "warning"
)
```

##### set_alpha(value: int)

Define a transparência da janela (0-100).

```python
menu.set_alpha(80)  # 80% de opacidade
```

##### toggle_visibility()

Alterna visibilidade do menu (mostrar/ocultar).

```python
menu.toggle_visibility()
```

##### run(hotkey: str = "insert")

Inicia o loop principal da aplicação.

```python
menu.run("insert")  # Pressione INSERT para mostrar/ocultar
```

#### Atributos Públicos

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `data` | dict | Dicionário para armazenar dados do usuário |
| `theme` | str | Cor atual do tema |
| `bg_color` | str | Cor de fundo |
| `notif_manager` | NotificationManager | Gerenciador de notificações |

#### Exemplo Completo

```python
from cliv_gui import ClivMenu, ModernButton, ModernSlider

# Criar menu customizado
menu = ClivMenu(
    title="MEU APLICATIVO",
    theme_color="#e74c3c",
    bg_img_path="background.jpg",
    part_color="cyan",
    part_count=50,
    part_speed=(0.3, 1.0),
    enable_tray_icon=True
)

# Adicionar abas
main = menu.add_tab("PRINCIPAL")
settings = menu.add_tab("CONFIG")

# Adicionar componentes
ModernButton(main, "Executar", menu,
             callback=lambda: print("Executado!"),
             style="success")

ModernSlider(settings, "Volume", 0, 100, menu,
             default=50,
             callback=lambda v: print(f"Volume: {v}"))

# Iniciar
menu.run("f1")  # F1 para mostrar/ocultar
```

---

### 4.2 ProcessOverlay

Classe para criar overlays transparentes sobre processos Windows.

#### Construtor

```python
ProcessOverlay(
    process_name: str,
    bg_color: str = "#000000",
    alpha: float = 0.3
)
```

#### Parâmetros

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| `process_name` | str | (obrigatório) | Nome do processo (ex: "notepad.exe") |
| `bg_color` | str | "#000000" | Cor de fundo do overlay |
| `alpha` | float | 0.3 | Transparência (0.0 = invisível, 1.0 = opaco) |

#### Métodos de Desenho

##### draw_rectangle(x, y, width, height, color="red", thickness=2, fill=None)

Desenha um retângulo.

```python
rect_id = overlay.draw_rectangle(100, 100, 200, 150, "red", 3)
```

**Retorna:** ID do desenho (para remoção posterior)

##### draw_line(x1, y1, x2, y2, color="red", thickness=2)

Desenha uma linha.

```python
line_id = overlay.draw_line(0, 0, 500, 500, "lime", 2)
```

##### draw_circle(x, y, radius, color="red", thickness=2, fill=None)

Desenha um círculo.

```python
circle_id = overlay.draw_circle(300, 200, 50, "yellow", 2)
```

##### draw_text(x, y, text, color="white", font=("Arial", 12, "bold"))

Desenha texto.

```python
text_id = overlay.draw_text(150, 100, "PLAYER", "red", ("Arial", 14, "bold"))
```

##### draw_crosshair(x, y, size=20, color="lime", thickness=2)

Desenha uma mira (crosshair).

```python
overlay.draw_crosshair(960, 540, size=30, color="cyan", thickness=2)
```

##### clear_drawings()

Remove todos os desenhos.

```python
overlay.clear_drawings()
```

##### delete_drawing(drawing_id)

Remove um desenho específico.

```python
overlay.delete_drawing(rect_id)
```

#### Métodos de Controle

##### set_alpha(alpha: float)

Ajusta a transparência do overlay.

```python
overlay.set_alpha(0.5)  # 50% transparente
```

##### start() -> bool

Inicia o overlay (sem bloquear).

```python
if overlay.start():
    print("Overlay iniciado!")
else:
    print("Processo não encontrado")
```

**Retorna:** True se bem-sucedido, False se processo não encontrado

##### stop()

Para o overlay.

```python
overlay.stop()
```

##### run()

Inicia o overlay e bloqueia até fechar.

```python
overlay.run()
```

#### Exemplo Completo - ESP de Jogo

```python
from cliv_gui import ProcessOverlay
import threading
import time

# Criar overlay
overlay = ProcessOverlay("game.exe", alpha=0.4)

# Lista de jogadores detectados
players = [
    {"x": 100, "y": 200, "name": "Enemy1", "health": 80},
    {"x": 300, "y": 150, "name": "Enemy2", "health": 50},
    {"x": 500, "y": 400, "name": "Teammate", "health": 100},
]

def draw_esp():
    """Loop de desenho do ESP"""
    while True:
        overlay.clear_drawings()

        for player in players:
            x, y = player["x"], player["y"]
            health = player["health"]

            # Cor baseada na saúde
            color = "lime" if health > 70 else "yellow" if health > 30 else "red"

            # Box ESP
            overlay.draw_rectangle(x, y, 60, 120, color, 2)

            # Nome do jogador
            overlay.draw_text(x+30, y-20, player["name"], color,
                            ("Arial", 10, "bold"))

            # Barra de vida
            health_width = int(60 * (health / 100))
            overlay.draw_rectangle(x, y-10, health_width, 5,
                                 "lime", 0, fill="lime")

            # Linha para o centro
            overlay.draw_line(x+30, y+120, 960, 540, color, 1)

        # Crosshair central
        overlay.draw_crosshair(960, 540, 20, "cyan", 2)

        time.sleep(0.016)  # ~60 FPS

# Iniciar loop de desenho em thread separada
threading.Thread(target=draw_esp, daemon=True).start()

# Iniciar overlay
overlay.run()
```

---

### 4.3 NotificationManager

Gerenciador de notificações toast.

#### Uso Básico

Geralmente usado através de `menu.show_notification()`, mas pode ser usado independentemente:

```python
from cliv_gui import NotificationManager

notif = NotificationManager()

notif.show(
    title="Alerta",
    message="Sistema atualizado com sucesso!",
    duration=3000,
    notification_type="success"
)
```

#### Tipos de Notificação

| Tipo | Cor | Ícone | Uso |
|------|-----|-------|-----|
| `info` | Azul (#3498db) | ℹ | Informações gerais |
| `success` | Verde (#2ecc71) | ✓ | Operações bem-sucedidas |
| `warning` | Laranja (#f39c12) | ⚠ | Avisos e alertas |
| `error` | Vermelho (#e74c3c) | ✕ | Erros e falhas |

#### Características

- ✨ Animações suaves (slide + fade)
- 📊 Barra de progresso automática
- 📚 Empilhamento inteligente
- 🔒 Thread-safe
- ⚡ Auto-reposicionamento ao fechar

---

### 4.4 MessageBox

Caixas de diálogo modais personalizadas.

#### Uso

```python
from cliv_gui import MessageBox

MessageBox.show(
    title="Confirmação",
    message="Deseja realmente sair?",
    msg_type="question",
    theme_color="#8e44ad"
)
```

#### Tipos Disponíveis

- `info` - Informação
- `success` - Sucesso
- `warning` - Aviso
- `error` - Erro
- `question` - Pergunta

#### Características

- 🎨 Estilo moderno sem bordas
- 🖱️ Draggable (pode arrastar)
- ✨ Animação fade-in
- 🎯 Modal (bloqueia interação com janela pai)

---

### 4.5 Componentes UI

#### 4.5.1 ModernButton

Botão estilizado com efeitos hover.

```python
from cliv_gui import ModernButton

ModernButton(
    container=tab,
    text="EXECUTAR",
    menu_ref=menu,
    callback=on_click,
    style="success"
)
```

**Estilos disponíveis:** `primary`, `success`, `danger`, `warning`, `info`

#### 4.5.2 ModernCheck

Checkbox customizado.

```python
from cliv_gui import ModernCheck

checkbox = ModernCheck(
    container=tab,
    text="Ativar Wallhack",
    menu_ref=menu,
    default=False,
    callback=lambda checked: print(f"Wallhack: {checked}")
)

# Obter estado
is_checked = checkbox.get_value()
```

#### 4.5.3 ModernSlider

Slider de valores numéricos.

```python
from cliv_gui import ModernSlider

slider = ModernSlider(
    container=tab,
    text="FOV",
    de=60,
    ate=120,
    menu_ref=menu,
    default=90,
    callback=lambda val: set_fov(val)
)

# Obter valor
current_fov = slider.get_value()
```

#### 4.5.4 DynamicColorPicker

Seletor de cores HSV com roda de cores.

```python
from cliv_gui import DynamicColorPicker

picker = DynamicColorPicker(
    container=tab,
    var_name="ESP_COLOR",
    menu_ref=menu
)

# Cor é armazenada automaticamente em menu.data
cor_selecionada = menu.data["ESP_COLOR"]  # Ex: "#ff0000"
```

#### 4.5.5 KeyBind

Captura de teclas para hotkeys.

```python
from cliv_gui import KeyBind

keybind = KeyBind(
    container=tab,
    text="Aimbot Key",
    var_name="AIM_KEY",
    menu_ref=menu,
    default="MOUSE5"
)

# Acessar tecla configurada
key = menu.data["AIM_KEY"]
```

#### 4.5.6 ModernGraph

Gráfico em tempo real.

```python
from cliv_gui import ModernGraph

graph = ModernGraph(
    container=tab,
    label="FPS",
    menu_ref=menu
)

# Adicionar valores
def update():
    graph.add_value(get_current_fps())
    menu.root.after(1000, update)

update()
```

#### 4.5.7 AudioPlayer

Player de áudio completo.

```python
from cliv_gui import AudioPlayer

player = AudioPlayer(
    container=tab,
    menu_ref=menu,
    audio_path="music.mp3",
    autoplay=True,
    loop=True
)

# Controlar
player.play_music()
player.pause_music()
player.stop_music()
player.set_volume(0.7)

# Obter status
status = player.get_status()
# {'playing': True, 'loop': True, 'volume': 0.7, 'file': 'music.mp3'}
```

#### 4.5.8 ImageSeparator

Separador visual com ícone e texto.

```python
from cliv_gui import ImageSeparator

ImageSeparator(
    container=tab,
    text="CONFIGURAÇÕES GRÁFICAS",
    icon_path="icon.png",
    menu_ref=menu
)
```

---

## 5. Guias Práticos

### 5.1 Criando Seu Primeiro Menu

**Passo 1:** Importar biblioteca

```python
from cliv_gui import ClivMenu, ModernButton, ModernCheck
```

**Passo 2:** Criar menu

```python
menu = ClivMenu(title="MEU APP", theme_color="#3498db")
```

**Passo 3:** Adicionar aba

```python
main_tab = menu.add_tab("PRINCIPAL")
```

**Passo 4:** Adicionar componentes

```python
ModernCheck(main_tab, "Feature 1", menu, default=True)
ModernButton(main_tab, "Executar", menu,
             callback=lambda: print("Executado!"))
```

**Passo 5:** Iniciar

```python
menu.run()
```

### 5.2 Trabalhando com Notificações

```python
# Notificação simples
menu.show_notification("Info", "Processo iniciado", 2000, "info")

# Com callback
def on_complete():
    menu.show_notification("Sucesso", "Tarefa concluída!", 3000, "success")

# Notificações sequenciais
for i in range(3):
    menu.show_notification(f"Etapa {i+1}", f"Processando...", 2000, "info")
```

### 5.3 Criando ESP para Jogos

```python
from cliv_gui import ProcessOverlay
import threading

overlay = ProcessOverlay("game.exe", alpha=0.3)

def draw_loop():
    while True:
        overlay.clear_drawings()

        # Buscar posições dos jogadores (implementar detecção)
        players = get_player_positions()

        for player in players:
            x, y = player['position']

            # Box ESP
            overlay.draw_rectangle(x-30, y-60, 60, 120, "red", 2)

            # Nome
            overlay.draw_text(x, y-70, player['name'], "white")

        time.sleep(0.016)  # 60 FPS

threading.Thread(target=draw_loop, daemon=True).start()
overlay.run()
```

### 5.4 Sistema de Configurações

```python
from cliv_gui import ClivMenu, ModernSlider, ModernCheck
import json

menu = ClivMenu(title="CONFIGURAÇÕES")
settings_tab = menu.add_tab("SETTINGS")

# Criar componentes
fov_slider = ModernSlider(settings_tab, "FOV", 60, 120, menu, default=90)
vsync_check = ModernCheck(settings_tab, "V-Sync", menu, default=True)

# Função para salvar
def save_settings():
    config = {
        'fov': fov_slider.get_value(),
        'vsync': vsync_check.get_value()
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)

    menu.show_notification("Config", "Salvo com sucesso!", 2000, "success")

# Botão salvar
ModernButton(settings_tab, "Salvar", menu,
             callback=save_settings, style="success")

menu.run()
```

### 5.5 Integração com System Tray

```python
menu = ClivMenu(
    title="MEU APP",
    enable_tray_icon=True,
    tray_icon_path="icon.ico"
)

# Quando minimizar, vai para a bandeja
# Clique duplo no ícone para restaurar
# Botão direito para menu de contexto

menu.run()
```

---

## 6. Exemplos Avançados

### 6.1 Dashboard de Sistema Completo

```python
from cliv_gui import ClivMenu, ModernGraph, ModernButton
import psutil
import threading

menu = ClivMenu(title="MONITOR DO SISTEMA", theme_color="#2ecc71")
monitor_tab = menu.add_tab("MONITOR")

# Gráficos
cpu_graph = ModernGraph(monitor_tab, "CPU %", menu)
ram_graph = ModernGraph(monitor_tab, "RAM %", menu)
disk_graph = ModernGraph(monitor_tab, "DISCO %", menu)

# Atualização em tempo real
def update_stats():
    while True:
        cpu_graph.add_value(psutil.cpu_percent())
        ram_graph.add_value(psutil.virtual_memory().percent)
        disk_graph.add_value(psutil.disk_usage('/').percent)
        time.sleep(1)

threading.Thread(target=update_stats, daemon=True).start()

# Botão para limpar cache
ModernButton(monitor_tab, "Limpar RAM", menu,
             callback=lambda: os.system("echo Limpeza simulada"),
             style="warning")

menu.run()
```

### 6.2 Ferramenta de Aimbot Visual

```python
from cliv_gui import ClivMenu, ProcessOverlay, ModernSlider, ModernCheck
import threading

# Menu de configuração
menu = ClivMenu(title="AIMBOT CONFIG")
config_tab = menu.add_tab("CONFIG")

# Configurações
fov_slider = ModernSlider(config_tab, "FOV", 1, 500, menu, default=120)
smooth_slider = ModernSlider(config_tab, "Suavização", 1, 20, menu, default=5)
aimbot_check = ModernCheck(config_tab, "Aimbot Ativado", menu, default=False)

# Overlay
overlay = ProcessOverlay("game.exe", alpha=0.3)

def draw_fov():
    while True:
        overlay.clear_drawings()

        if aimbot_check.get_value():
            # Desenhar FOV circle
            fov = fov_slider.get_value()
            overlay.draw_circle(960, 540, fov, "lime", 2)

            # Crosshair
            overlay.draw_crosshair(960, 540, 20, "red", 2)

            # Status
            overlay.draw_text(20, 20, "AIMBOT: ON", "lime", ("Arial", 14, "bold"))

        time.sleep(0.016)

# Iniciar overlay em thread
threading.Thread(target=draw_fov, daemon=True).start()

# Iniciar menu
menu.run()
```

### 6.3 Player de Música com Visualizador

```python
from cliv_gui import ClivMenu, AudioPlayer, ModernGraph
import random

menu = ClivMenu(title="MUSIC PLAYER", theme_color="#9b59b6")
player_tab = menu.add_tab("PLAYER")

# Player de áudio
audio = AudioPlayer(player_tab, menu, "music.mp3", autoplay=True)

# Visualizador
visualizer = ModernGraph(player_tab, "AUDIO VISUALIZER", menu)

# Simular visualização de áudio
def update_visualizer():
    while True:
        if audio.playing:
            # Simular amplitude de áudio
            amplitude = random.randint(20, 100)
            visualizer.add_value(amplitude)
        else:
            visualizer.add_value(0)

        time.sleep(0.05)

threading.Thread(target=update_visualizer, daemon=True).start()

menu.run()
```

### 6.4 Trainer de Jogo Completo

```python
from cliv_gui import (ClivMenu, ModernButton, ModernCheck,
                      ModernSlider, KeyBind, ImageSeparator)

menu = ClivMenu(title="GAME TRAINER", theme_color="#e74c3c")

# Aba: Cheats
cheats_tab = menu.add_tab("CHEATS")

ImageSeparator(cheats_tab, "PLAYER CHEATS", menu_ref=menu)
ModernCheck(cheats_tab, "God Mode", menu, default=False,
            callback=lambda v: activate_godmode(v))
ModernCheck(cheats_tab, "Infinite Ammo", menu)
ModernCheck(cheats_tab, "No Clip", menu)

ImageSeparator(cheats_tab, "VISUAL CHEATS", menu_ref=menu)
ModernCheck(cheats_tab, "ESP Players", menu)
ModernCheck(cheats_tab, "ESP Items", menu)

# Aba: Configurações
config_tab = menu.add_tab("CONFIG")

ModernSlider(config_tab, "Speed Multiplier", 1, 10, menu, default=1)
ModernSlider(config_tab, "Jump Height", 1, 100, menu, default=10)

# Aba: Hotkeys
hotkey_tab = menu.add_tab("HOTKEYS")

KeyBind(hotkey_tab, "God Mode Key", "GOD_KEY", menu, default="F1")
KeyBind(hotkey_tab, "ESP Key", "ESP_KEY", menu, default="F2")
KeyBind(hotkey_tab, "Speed Key", "SPEED_KEY", menu, default="F3")

# Aba: Info
info_tab = menu.add_tab("INFO")

ModernButton(info_tab, "Check for Updates", menu,
             callback=lambda: menu.show_notification("Update",
                                                     "Você está atualizado!",
                                                     2000, "success"),
             style="info")

ModernButton(info_tab, "Discord Server", menu,
             callback=lambda: os.system("start https://discord.gg/example"),
             style="primary")

menu.run()
```

---

## 7. Troubleshooting

### 7.1 Problemas Comuns

#### Erro: "No module named 'cliv_gui'"

**Solução:**
```bash
pip install --upgrade cliv-gui
```

#### Erro: "pygame.error: No available video device"

**Solução:**
```bash
pip uninstall pygame
pip install pygame --upgrade
```

#### Erro: "ImportError: DLL load failed"

**Causa:** pywin32 não instalado corretamente

**Solução:**
```bash
pip uninstall pywin32
pip install pywin32==304
python Scripts/pywin32_postinstall.py -install
```

#### Overlay não aparece

**Checklist:**
1. ✅ Processo está rodando?
2. ✅ Nome do processo está correto? (verificar no Task Manager)
3. ✅ Executando como administrador?
4. ✅ Janela do jogo está visível?

**Solução:**
```python
# Verificar se processo existe
import psutil

def check_process(name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == name.lower():
            print(f"Processo encontrado: {proc.pid}")
            return True
    print("Processo não encontrado!")
    return False

check_process("notepad.exe")
```

#### Notificações não aparecem

**Causa:** Outras janelas cobrindo ou múltiplos monitores

**Solução:**
```python
# Ajustar posição manualmente editando NotificationManager
# Linha ~45 em cliv_extreme_fixed.py
x = screen_width - width - 20  # Ajuste aqui
y = screen_height - height - 60 - offset  # E aqui
```

#### Menu não responde à hotkey

**Causa:** Permissões ou conflito de tecla

**Solução:**
```python
# Executar como administrador
# Ou usar tecla diferente
menu.run("f10")  # Ao invés de INSERT
```

### 7.2 Debug Mode

Para debug, ative prints extras:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Agora todas as operações serão logadas
```

### 7.3 Performance

Se o menu estiver lento:

```python
# Reduzir partículas
menu = ClivMenu(part_count=10)  # Menos partículas

# Desabilitar partículas
menu = ClivMenu(part_count=0)

# Reduzir FPS do overlay
# Em draw_loop(), aumentar sleep:
time.sleep(0.033)  # 30 FPS ao invés de 60
```

---

## 8. Best Practices

### 8.1 Estrutura de Código

```python
# ✅ BOM - Organizado
class MyApp:
    def __init__(self):
        self.menu = ClivMenu(title="MY APP")
        self.setup_ui()

    def setup_ui(self):
        self.create_tabs()
        self.add_components()

    def create_tabs(self):
        self.main_tab = self.menu.add_tab("MAIN")
        self.config_tab = self.menu.add_tab("CONFIG")

    def add_components(self):
        ModernButton(self.main_tab, "Start", self.menu,
                    callback=self.on_start)

    def on_start(self):
        print("Started!")

    def run(self):
        self.menu.run()

app = MyApp()
app.run()
```

```python
# ❌ RUIM - Desorganizado
menu = ClivMenu(title="MY APP")
tab1 = menu.add_tab("MAIN")
ModernButton(tab1, "Start", menu, callback=lambda: print("Started!"))
tab2 = menu.add_tab("CONFIG")
# ... código espalhado
menu.run()
```

### 8.2 Gerenciamento de Estado

```python
# ✅ BOM - Usar menu.data
menu.data['esp_enabled'] = True
menu.data['fov'] = 120

# Acessar de callbacks
def toggle_esp(checked):
    menu.data['esp_enabled'] = checked
    update_esp()
```

```python
# ❌ RUIM - Variáveis globais
esp_enabled = True
fov = 120

def toggle_esp(checked):
    global esp_enabled
    esp_enabled = checked
```

### 8.3 Threading

```python
# ✅ BOM - Daemon threads
def background_task():
    while True:
        do_something()
        time.sleep(1)

thread = threading.Thread(target=background_task, daemon=True)
thread.start()
```

```python
# ❌ RUIM - Thread sem daemon
thread = threading.Thread(target=background_task)
thread.start()
# Thread continua rodando após fechar menu!
```

### 8.4 Tratamento de Erros

```python
# ✅ BOM - Com try/except
def safe_operation():
    try:
        result = risky_function()
        menu.show_notification("Sucesso", "OK!", 2000, "success")
    except Exception as e:
        menu.show_notification("Erro", str(e), 3000, "error")
        logging.error(f"Erro: {e}")
```

```python
# ❌ RUIM - Sem tratamento
def unsafe_operation():
    result = risky_function()  # Pode crashar o programa!
```

### 8.5 Limpeza de Recursos

```python
# ✅ BOM - Limpar ao fechar
def on_close():
    stop_threads()
    save_config()
    overlay.stop()
    menu._on_close()

# Sobrescrever método de fechamento
menu._on_close = on_close
```

---

## 9. FAQ

### 9.1 Geral

**P: ClivGui funciona em Linux/Mac?**
R: Não, é exclusivo para Windows devido ao uso de APIs do Windows (pywin32).

**P: Posso usar para aplicações comerciais?**
R: Sim! A licença MIT permite uso comercial.

**P: Como compilar para .exe?**
R: Use PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole meu_app.py
```

**P: Qual a diferença entre ClivMenu e ProcessOverlay?**
R: ClivMenu é o menu de configuração. ProcessOverlay é o overlay transparente sobre jogos/apps.

### 9.2 Técnicas

**P: Como fazer o overlay seguir um objeto específico?**
R: Atualize as coordenadas em tempo real:
```python
def track_object():
    while True:
        x, y = get_object_position()
        overlay.clear_drawings()
        overlay.draw_circle(x, y, 50, "red", 2)
        time.sleep(0.016)
```

**P: Como salvar configurações?**
R: Use JSON:
```python
import json

# Salvar
with open('config.json', 'w') as f:
    json.dump(menu.data, f)

# Carregar
with open('config.json', 'r') as f:
    menu.data = json.load(f)
```

**P: Como adicionar ícone customizado ao menu?**
R: Defina o ícone da janela:
```python
menu.root.iconbitmap('icon.ico')
```

**P: Como mudar tema dinamicamente?**
R: Atualize a cor e recrie componentes:
```python
menu.theme = "#e74c3c"
# Recriar componentes necessários
```

### 9.3 Troubleshooting

**P: Por que o menu não aparece?**
R: Verifique se está chamando `menu.run()` e se não há erros no console.

**P: Hotkey não funciona?**
R: Execute como administrador ou use uma tecla diferente.

**P: Overlay aparece atrás da janela do jogo?**
R: Certifique-se que o jogo não está em fullscreen exclusivo. Use borderless windowed.

**P: Notificações sobrepõem outras janelas?**
R: É o comportamento esperado (topmost). Para desabilitar:
```python
# Editar NotificationManager, remover:
# notif.attributes("-topmost", True)
```

---

## 📚 Recursos Adicionais

- **GitHub:** https://github.com/Nigth613/ClivGui
- **Exemplos:** https://github.com/Night613/ClivGui/tree/main/examples
- **Issues:** https://github.com/Nigth613/ClivGui/issues
- **Contato:** clivguicontact@gmail.com

---

## 📄 Licença

ClivGui é licenciado sob a MIT License.

Copyright © 2026 Night613

---

**Última atualização:** 07/02/2026
**Versão da documentação:** 1.0.0
