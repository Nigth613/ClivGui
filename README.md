# 📖 ClivGui - Documentação Completa

**Versão:** 1.0.4
**Última Atualização:** 08/02/2026
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
   - [WidgetStyle](#45-widgetstyle)
   - [Componentes UI](#46-componentes-ui)
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
| **Audio Player** | Player de áudio integrado com controles completos |
| **Color Picker** | Seletor HSV com roda de cores dinâmica |
| **System Tray** | Integração com bandeja do sistema |
| **Thread-Safe** | Seguro para uso com múltiplas threads |
| **Sistema de Estilos** | WidgetStyle para personalização avançada |
| **Flexível** | Modo com ou sem abas |

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
# O módulo deve importar sem erros
```

---

## 3. Conceitos Básicos

### 3.1 Estrutura de um Projeto ClivGui

**Modo sem abas (simples):**
```python
from cliv_gui import ClivMenu, ModernButton

# 1. Criar menu sem abas
menu = ClivMenu(title="MEU APP", theme_color="#8e44ad", enable_tabs=False)

# 2. Obter container principal
container = menu.get_container()

# 3. Adicionar componentes
ModernButton(container, "Clique Aqui", menu,
             callback=lambda: print("Clicado!"))

# 4. Iniciar aplicação
menu.run()
```

**Modo com abas (organizado):**
```python
from cliv_gui import ClivMenu, ModernButton

# 1. Criar menu com abas (padrão)
menu = ClivMenu(title="MEU APP", theme_color="#8e44ad")

# 2. Adicionar abas
tab1 = menu.add_tab("PRINCIPAL")
tab2 = menu.add_tab("CONFIGURAÇÕES")

# 3. Adicionar componentes em cada aba
ModernButton(tab1, "Executar", menu, callback=lambda: print("Executado!"))
ModernButton(tab2, "Salvar", menu, callback=lambda: print("Salvo!"))

# 4. Iniciar aplicação
menu.run()
```

### 3.2 Fluxo de Trabalho

```
┌─────────────────────┐
│  Criar ClivMenu     │
│  (com ou sem tabs)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Obter Container     │
│ get_container() ou  │
│ add_tab("Nome")     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Adicionar           │
│ Componentes         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   menu.run()        │
└─────────────────────┘
```

### 3.3 Sistema de Abas (Opcional)

- **Com abas (`enable_tabs=True`):** Ideal para aplicações complexas com múltiplas seções
- **Sem abas (`enable_tabs=False`):** Ideal para aplicações simples com poucos controles

```python
# Com abas (padrão)
menu = ClivMenu(title="APP COMPLEXO")
main_tab = menu.add_tab("PRINCIPAL")
settings_tab = menu.add_tab("CONFIGURAÇÕES")
about_tab = menu.add_tab("SOBRE")

# Sem abas
menu = ClivMenu(title="APP SIMPLES", enable_tabs=False)
container = menu.get_container()
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
    width=450,
    height=720,
    part_color="white",
    part_count=40,
    part_speed=(0.2, 0.8),
    enable_tray_icon=False,
    tray_icon_path=None,
    enable_tabs=True
)
```

#### Parâmetros

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| `title` | str | "CLIV1 EXTREME" | Título da janela |
| `theme_color` | str | "#8e44ad" | Cor do tema em hexadecimal |
| `bg_img_path` | str | None | Caminho para imagem de fundo |
| `width` | int | 450 | Largura da janela em pixels |
| `height` | int | 720 | Altura da janela em pixels |
| `part_color` | str | "white" | Cor das partículas animadas |
| `part_count` | int | 40 | Quantidade de partículas (0 para desabilitar) |
| `part_speed` | tuple | (0.2, 0.8) | Velocidade mín/máx das partículas |
| `enable_tray_icon` | bool | False | Habilitar ícone na bandeja |
| `tray_icon_path` | str | None | Caminho do ícone customizado |
| `enable_tabs` | bool | True | Habilitar sistema de abas |

#### Métodos Principais

##### get_container() -> Frame

**NOVO:** Retorna o container principal para adicionar widgets. Funciona tanto com abas quanto sem abas.

```python
# Sem abas
menu = ClivMenu(enable_tabs=False)
container = menu.get_container()
ModernButton(container, "Botão", menu)

# Com abas (cria aba padrão se necessário)
menu = ClivMenu(enable_tabs=True)
container = menu.get_container()  # Retorna primeira aba ou cria "Main"
```

**Retorna:** Frame do Tkinter onde componentes podem ser adicionados

##### add_tab(name: str) -> Frame

Adiciona uma nova aba ao menu (apenas se `enable_tabs=True`).

```python
tab = menu.add_tab("CONFIGURAÇÕES")
```

**Retorna:** Frame do Tkinter onde componentes podem ser adicionados
**Exceção:** Lança `RuntimeError` se `enable_tabs=False`

##### show_tab(name: str)

Exibe uma aba específica (apenas se `enable_tabs=True`).

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

**Tipos disponíveis:** `"info"`, `"success"`, `"warning"`, `"error"`, `"question"`

##### set_alpha(value: float)

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
| `root` | tk.Tk | Janela principal do Tkinter |
| `data` | dict | Dicionário para armazenar dados do usuário |
| `theme` | str | Cor atual do tema |
| `bg_color` | str | Cor de fundo ("#05050a") |
| `notif_manager` | NotificationManager | Gerenciador de notificações |
| `main_container` | tk.Frame | Container principal (quando enable_tabs=False) |
| `abas` | dict | Dicionário de abas (quando enable_tabs=True) |
| `enable_tabs` | bool | Se o sistema de abas está habilitado |

#### Exemplo Completo

```python
from cliv_gui import ClivMenu, ModernButton, ModernSlider, ModernCheck

# Criar menu customizado
menu = ClivMenu(
    title="MEU APLICATIVO",
    theme_color="#e74c3c",
    bg_img_path="background.jpg",
    width=500,
    height=800,
    part_color="cyan",
    part_count=50,
    part_speed=(0.3, 1.0),
    enable_tray_icon=True,
    enable_tabs=True
)

# Adicionar abas
main = menu.add_tab("PRINCIPAL")
settings = menu.add_tab("CONFIG")

# Adicionar componentes
ModernButton(main, "Executar", menu,
             callback=lambda: print("Executado!"),
             button_style="success")

ModernSlider(settings, "Volume", 0, 100, menu,
             default=50,
             callback=lambda v: print(f"Volume: {v}"))

ModernCheck(settings, "Auto-Save", menu,
            default=True,
            callback=lambda v: print(f"Auto-Save: {v}"))

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

**Exceção:** Lança `ValueError` se alpha não estiver entre 0.0 e 1.0

#### Métodos de Desenho

##### draw_rectangle(x, y, width, height, color="red", thickness=2, fill=None) -> int

Desenha um retângulo.

```python
rect_id = overlay.draw_rectangle(100, 100, 200, 150, "red", 3)
```

**Retorna:** ID do desenho (para remoção posterior)

##### draw_line(x1, y1, x2, y2, color="red", thickness=2) -> int

Desenha uma linha.

```python
line_id = overlay.draw_line(0, 0, 500, 500, "lime", 2)
```

##### draw_circle(x, y, radius, color="red", thickness=2, fill=None) -> int

Desenha um círculo.

```python
circle_id = overlay.draw_circle(300, 200, 50, "yellow", 2, fill="yellow")
```

##### draw_text(x, y, text, color="white", font=("Arial", 12, "bold")) -> int

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

##### delete_drawing(drawing_id: int)

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

**Exceção:** Lança `ValueError` se alpha não estiver entre 0.0 e 1.0

##### start() -> bool

Inicia o overlay (sem bloquear).

```python
if overlay.start():
    print("Overlay iniciado!")
else:
    print("Processo não encontrado")
```

**Retorna:** `True` se bem-sucedido, `False` se processo não encontrado

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

#### Métodos Internos

##### find_process_window() -> Optional[int]

Encontra a janela do processo pelo nome.

**Retorna:** Handle da janela (HWND) ou None se não encontrado

##### get_window_rect(hwnd: int) -> Optional[Tuple[int, int, int, int]]

Obtém posição e tamanho da janela.

**Retorna:** Tupla (x, y, width, height) ou None

##### update_position()

Atualiza posição do overlay para seguir a janela do processo. Chamado automaticamente a cada 16ms (~60 FPS).

#### Exemplo Completo - ESP de Jogo

```python
from cliv_gui import ProcessOverlay
import threading
import time

# Criar overlay
overlay = ProcessOverlay("game.exe", alpha=0.4)

# Lista de jogadores detectados (exemplo)
players = [
    {"x": 100, "y": 200, "name": "Enemy1", "health": 80, "distance": 50},
    {"x": 300, "y": 150, "name": "Enemy2", "health": 50, "distance": 75},
    {"x": 500, "y": 400, "name": "Teammate", "health": 100, "distance": 30},
]

def draw_esp():
    """Loop de desenho do ESP"""
    while True:
        overlay.clear_drawings()

        for player in players:
            x, y = player["x"], player["y"]
            health = player["health"]
            distance = player["distance"]

            # Cor baseada na saúde
            if health > 70:
                color = "lime"
            elif health > 30:
                color = "yellow"
            else:
                color = "red"

            # Box ESP
            overlay.draw_rectangle(x, y, 60, 120, color, 2)

            # Nome do jogador
            overlay.draw_text(x+30, y-20, player["name"], color,
                            ("Arial", 10, "bold"))

            # Distância
            overlay.draw_text(x+30, y-35, f"{distance}m", "white",
                            ("Arial", 8))

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

Gerenciador de notificações toast estilo Roblox/Discord.

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

#### Método Principal

##### show(title: str, message: str, duration: int = 3000, notification_type: str = "info") -> tk.Toplevel

Mostra uma notificação no canto inferior direito.

**Retorna:** Janela da notificação ou None em caso de erro

#### Tipos de Notificação

| Tipo | Cor | Uso |
|------|-----|-----|
| `info` | Azul (#3498db) | Informações gerais |
| `success` | Verde (#2ecc71) | Operações bem-sucedidas |
| `warning` | Laranja (#f39c12) | Avisos e alertas |
| `error` | Vermelho (#e74c3c) | Erros e falhas |

#### Características

- ✨ Animações suaves (slide + fade)
- 📊 Barra de progresso automática
- 📚 Empilhamento inteligente (até múltiplas notificações)
- 🔒 Thread-safe com locks
- ⚡ Auto-reposicionamento ao fechar
- 🎯 Easing functions (cubic)
- ✕ Botão de fechar manual

#### Métodos Internos

- `_animate_in()`: Animação de entrada
- `_animate_out()`: Animação de saída
- `_close_notification()`: Fecha com animação
- `_reposition_notifications()`: Reposiciona após fechamento
- `_smooth_move()`: Move suavemente para nova posição
- `_start_progress_fixed()`: Anima barra de progresso

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

#### Método Estático

##### show(title: str, message: str, msg_type: str = "info", theme_color: str = "#8e44ad") -> None

Exibe um messagebox modal.

#### Tipos Disponíveis

| Tipo | Ícone | Cor Padrão |
|------|-------|------------|
| `info` | ℹ | #3498db |
| `success` | ✓ | #2ecc71 |
| `warning` | ⚠ | #f39c12 |
| `error` | ✕ | #e74c3c |
| `question` | ? | #9b59b6 |

#### Características

- 🎨 Estilo moderno sem bordas
- 🖱️ Draggable (pode arrastar pela barra superior)
- ✨ Animação fade-in suave
- 🎯 Modal (bloqueia interação com janela pai)
- 📐 Centralizado na tela
- ⌨️ Suporte a `grab_set()` para foco

---

### 4.5 WidgetStyle

**NOVO:** Dataclass para configuração de estilo de widgets.

#### Estrutura

```python
@dataclass
class WidgetStyle:
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
```

#### Uso

```python
from cliv_gui import WidgetStyle, ModernButton

# Criar estilo customizado
custom_style = WidgetStyle(
    bg_color="#2c3e50",
    fg_color="#ecf0f1",
    font=("Arial", 11, "bold"),
    padding=(15, 15, 15, 15),
    margin=(10, 10, 10, 10)
)

# Aplicar a um widget
ModernButton(container, "Botão Customizado", menu,
             style=custom_style)

# Posicionamento absoluto
absolute_style = WidgetStyle(
    pack=False,
    x=100,
    y=50,
    width=200,
    height=40
)

ModernButton(container, "Botão Posicionado", menu,
             style=absolute_style)
```

---

### 4.6 Componentes UI

#### 4.6.1 ModernButton

Botão estilizado com efeitos hover.

```python
ModernButton(
    container: tk.Frame,
    text: str,
    menu_ref: ClivMenu,
    callback: Optional[Callable] = None,
    button_style: str = "primary",
    style: Optional[WidgetStyle] = None
)
```

**Estilos disponíveis:**
- `primary`: Cor do tema
- `success`: Verde (#2ecc71)
- `danger`: Vermelho (#e74c3c)
- `warning`: Laranja (#f39c12)
- `info`: Azul (#3498db)

**Exemplo:**
```python
ModernButton(tab, "EXECUTAR", menu,
             callback=lambda: print("Executado!"),
             button_style="success")
```

#### 4.6.2 ModernCheck

Checkbox customizado com canvas.

```python
ModernCheck(
    container: tk.Frame,
    text: str,
    menu_ref: ClivMenu,
    default: bool = False,
    callback: Optional[Callable[[bool], None]] = None,
    style: Optional[WidgetStyle] = None
)
```

**Métodos:**
- `get_value()`: Retorna estado atual (bool)
- `set_value(value: bool)`: Define estado
- `toggle()`: Alterna estado

**Exemplo:**
```python
checkbox = ModernCheck(tab, "Ativar Wallhack", menu,
                       default=False,
                       callback=lambda v: print(f"Wallhack: {v}"))

# Obter estado
is_checked = checkbox.get_value()
```

#### 4.6.3 ModernSlider

Slider de valores numéricos com thumb animado.

```python
ModernSlider(
    container: tk.Frame,
    text: str,
    de: int,
    ate: int,
    menu_ref: ClivMenu,
    default: Optional[int] = None,
    callback: Optional[Callable[[int], None]] = None,
    style: Optional[WidgetStyle] = None
)
```

**Métodos:**
- `get_value()`: Retorna valor atual (int)
- `set_value(value: int)`: Define valor

**Exemplo:**
```python
slider = ModernSlider(tab, "FOV", 60, 120, menu,
                      default=90,
                      callback=lambda val: set_fov(val))

# Obter valor
current_fov = slider.get_value()

# Definir valor programaticamente
slider.set_value(100)
```

#### 4.6.4 DynamicColorPicker

Seletor de cores HSV com roda de cores.

```python
DynamicColorPicker(
    container: tk.Frame,
    var_name: str,
    menu_ref: ClivMenu,
    style: Optional[WidgetStyle] = None,
    callback: Optional[Callable[[str], None]] = None
)
```

**Características:**
- Roda de cores HSV visual
- Barras de saturação e valor (brightness)
- Preview da cor selecionada
- Armazenamento automático em `menu.data[var_name]`

**Métodos:**
- `get_color()`: Retorna cor em formato hex (#RRGGBB)

**Exemplo:**
```python
picker = DynamicColorPicker(tab, "ESP_COLOR", menu,
                            callback=lambda color: print(f"Cor: {color}"))

# Cor é armazenada automaticamente
cor_selecionada = menu.data["ESP_COLOR"]  # Ex: "#ff0000"

# Ou obter diretamente
cor = picker.get_color()
```

#### 4.6.5 KeyBind

Captura de teclas para hotkeys.

```python
KeyBind(
    container: tk.Frame,
    text: str,
    var_name: str,
    menu_ref: ClivMenu,
    default: str = "NONE",
    callback: Optional[Callable[[str], None]] = None,
    style: Optional[WidgetStyle] = None
)
```

**Métodos:**
- `get_key()`: Retorna tecla atual (str)
- `start_listen()`: Inicia escuta manual

**Exemplo:**
```python
keybind = KeyBind(tab, "Aimbot Key", "AIM_KEY", menu,
                  default="MOUSE5",
                  callback=lambda key: print(f"Nova tecla: {key}"))

# Acessar tecla configurada
key = menu.data["AIM_KEY"]
# Ou
key = keybind.get_key()
```

#### 4.6.6 ModernGraph

Gráfico de linhas em tempo real.

```python
ModernGraph(
    container: tk.Frame,
    label: str,
    menu_ref: ClivMenu,
    style: Optional[WidgetStyle] = None,
    max_values: int = 50
)
```

**Métodos:**
- `add_value(val: float)`: Adiciona valor ao gráfico

**Características:**
- Grid de fundo
- Linha suavizada
- Preenchimento gradiente
- Auto-scroll (mantém últimos max_values)

**Exemplo:**
```python
graph = ModernGraph(tab, "CPU USAGE %", menu, max_values=60)

# Adicionar valores em loop
def update():
    import psutil
    graph.add_value(psutil.cpu_percent())
    menu.root.after(1000, update)

update()
```

#### 4.6.7 AudioPlayer

Player de áudio completo com controles.

```python
AudioPlayer(
    container: tk.Frame,
    menu_ref: ClivMenu,
    audio_path: str = "music.mp3",
    autoplay: bool = False,
    loop: bool = True,
    style: Optional[WidgetStyle] = None
)
```

**Métodos:**
- `play_music()`: Inicia/resume reprodução
- `pause_music()`: Pausa reprodução
- `stop_music()`: Para completamente
- `set_volume(event)`: Define volume (0.0 a 1.0)
- `toggle_play()`: Alterna play/pause
- `toggle_loop()`: Alterna modo loop
- `set_audio_file(path: str)`: Muda arquivo de áudio
- `get_status()`: Retorna dict com status atual

**Características:**
- Controles play/pause/stop
- Barra de volume visual e interativa
- Botão de loop
- Indicador de status (LED)
- Notificações de eventos

**Exemplo:**
```python
player = AudioPlayer(tab, menu,
                     audio_path="music.mp3",
                     autoplay=True,
                     loop=True)

# Controlar programaticamente
player.set_volume_value(0.7)  # Usar set_volume() com event mock
player.play_music()
player.pause_music()
player.stop_music()

# Obter status
status = player.get_status()
# {'playing': True, 'loop': True, 'volume': 0.7, 'file': 'music.mp3'}

# Mudar música
player.set_audio_file("outro.mp3")
```

#### 4.6.8 ImageSeparator

Separador visual com ícone e texto opcional.

```python
ImageSeparator(
    container: tk.Frame,
    text: str,
    icon_path: Optional[str] = None,
    menu_ref: Optional[ClivMenu] = None,
    style: Optional[WidgetStyle] = None
)
```

**Exemplo:**
```python
ImageSeparator(tab, "CONFIGURAÇÕES GRÁFICAS",
               icon_path="icon.png",
               menu_ref=menu)

# Sem ícone
ImageSeparator(tab, "SEÇÃO 2", menu_ref=menu)
```

---

## 5. Guias Práticos

### 5.1 Criando Seu Primeiro Menu

**Passo 1:** Importar biblioteca

```python
from cliv_gui import ClivMenu, ModernButton, ModernCheck
```

**Passo 2:** Criar menu (escolher modo)

```python
# Modo simples (sem abas)
menu = ClivMenu(title="MEU APP", theme_color="#3498db", enable_tabs=False)
container = menu.get_container()

# OU modo organizado (com abas)
menu = ClivMenu(title="MEU APP", theme_color="#3498db")
main_tab = menu.add_tab("PRINCIPAL")
```

**Passo 3:** Adicionar componentes

```python
ModernCheck(container, "Feature 1", menu, default=True)
ModernButton(container, "Executar", menu,
             callback=lambda: print("Executado!"),
             button_style="success")
```

**Passo 4:** Iniciar

```python
menu.run("insert")
```

### 5.2 Trabalhando com Notificações

```python
# Notificação simples
menu.show_notification("Info", "Processo iniciado", 2000, "info")

# Com callback
def on_complete():
    menu.show_notification("Sucesso", "Tarefa concluída!", 3000, "success")

# Notificações sequenciais (empilham automaticamente)
for i in range(3):
    menu.show_notification(f"Etapa {i+1}", f"Processando...", 2000, "info")

# Diferentes tipos
menu.show_notification("Erro", "Falha na conexão", 5000, "error")
menu.show_notification("Atenção", "Trial expira em 3 dias", 4000, "warning")
```

### 5.3 Criando ESP para Jogos

```python
from cliv_gui import ProcessOverlay
import threading
import time

overlay = ProcessOverlay("game.exe", alpha=0.3)

def draw_loop():
    while True:
        overlay.clear_drawings()

        # Buscar posições dos jogadores (implementar detecção)
        players = get_player_positions()  # Sua função de detecção

        for player in players:
            x, y = player['position']
            health = player.get('health', 100)
            name = player.get('name', 'UNKNOWN')

            # Cor baseada na saúde
            color = "lime" if health > 70 else "yellow" if health > 30 else "red"

            # Box ESP
            overlay.draw_rectangle(x-30, y-60, 60, 120, color, 2)

            # Nome
            overlay.draw_text(x, y-70, name, color, ("Arial", 10, "bold"))

            # Barra de vida
            health_width = int(60 * (health / 100))
            overlay.draw_rectangle(x-30, y-75, health_width, 3,
                                 "lime", 0, fill="lime")

        # Crosshair central
        overlay.draw_crosshair(960, 540, 20, "cyan", 2)

        time.sleep(0.016)  # 60 FPS

threading.Thread(target=draw_loop, daemon=True).start()
overlay.run()
```

### 5.4 Sistema de Configurações com Persistência

```python
from cliv_gui import ClivMenu, ModernSlider, ModernCheck, ModernButton
import json
import os

menu = ClivMenu(title="CONFIGURAÇÕES")
settings_tab = menu.add_tab("SETTINGS")

# Criar componentes
fov_slider = ModernSlider(settings_tab, "FOV", 60, 120, menu, default=90)
vsync_check = ModernCheck(settings_tab, "V-Sync", menu, default=True)
fullscreen_check = ModernCheck(settings_tab, "Fullscreen", menu, default=False)

# Função para salvar
def save_settings():
    config = {
        'fov': fov_slider.get_value(),
        'vsync': vsync_check.get_value(),
        'fullscreen': fullscreen_check.get_value()
    }

    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)

        menu.show_notification("Config", "Salvo com sucesso!", 2000, "success")
    except Exception as e:
        menu.show_notification("Erro", f"Falha ao salvar: {e}", 3000, "error")

# Função para carregar
def load_settings():
    if not os.path.exists('config.json'):
        menu.show_notification("Config", "Arquivo não encontrado", 2000, "info")
        return

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)

        fov_slider.set_value(config.get('fov', 90))
        vsync_check.set_value(config.get('vsync', True))
        fullscreen_check.set_value(config.get('fullscreen', False))

        menu.show_notification("Config", "Carregado com sucesso!", 2000, "success")
    except Exception as e:
        menu.show_notification("Erro", f"Falha ao carregar: {e}", 3000, "error")

# Botões
ModernButton(settings_tab, "Salvar", menu,
             callback=save_settings, button_style="success")
ModernButton(settings_tab, "Carregar", menu,
             callback=load_settings, button_style="info")

# Carregar ao iniciar
menu.root.after(500, load_settings)

menu.run()
```

### 5.5 Integração com System Tray

```python
menu = ClivMenu(
    title="MEU APP",
    enable_tray_icon=True,
    tray_icon_path="icon.ico"  # Opcional, usa ícone padrão se None
)

# Quando minimizar, vai para a bandeja
# Clique duplo no ícone para restaurar
# Botão direito para menu de contexto com:
# - Mostrar/Ocultar
# - Notificação de Teste
# - Fechar

menu.run()
```

### 5.6 Usando WidgetStyle para Personalização

```python
from cliv_gui import WidgetStyle

# Estilo dark mode
dark_style = WidgetStyle(
    bg_color="#1a1a1a",
    fg_color="#ecf0f1",
    font=("Consolas", 10, "normal"),
    padding=(12, 12, 12, 12),
    margin=(8, 8, 8, 8)
)

# Aplicar a múltiplos widgets
ModernButton(tab, "Botão 1", menu, style=dark_style)
ModernCheck(tab, "Opção 1", menu, style=dark_style)
ModernSlider(tab, "Valor", 0, 100, menu, style=dark_style)

# Estilo com posicionamento absoluto
positioned_style = WidgetStyle(
    pack=False,
    x=50,
    y=100,
    width=300,
    height=50,
    bg_color="#2c3e50"
)

ModernButton(tab, "Posicionado", menu, style=positioned_style)
```

---

## 6. Exemplos Avançados

### 6.1 Dashboard de Sistema Completo

```python
from cliv_gui import ClivMenu, ModernGraph, ModernButton
import psutil
import threading
import time

menu = ClivMenu(title="MONITOR DO SISTEMA", theme_color="#2ecc71", width=600)
monitor_tab = menu.add_tab("MONITOR")

# Gráficos
cpu_graph = ModernGraph(monitor_tab, "CPU %", menu, max_values=60)
ram_graph = ModernGraph(monitor_tab, "RAM %", menu, max_values=60)
disk_graph = ModernGraph(monitor_tab, "DISCO C: %", menu, max_values=60)

# Flag para controlar thread
running = {'value': True}

# Atualização em tempo real
def update_stats():
    while running['value']:
        cpu_graph.add_value(psutil.cpu_percent(interval=0.1))
        ram_graph.add_value(psutil.virtual_memory().percent)
        disk_graph.add_value(psutil.disk_usage('C:/').percent)
        time.sleep(1)

# Iniciar thread
stats_thread = threading.Thread(target=update_stats, daemon=True)
stats_thread.start()

# Botões de controle
def clear_cache():
    menu.show_notification("Sistema", "Limpeza iniciada...", 2000, "info")
    # Implementar limpeza
    time.sleep(2)
    menu.show_notification("Sistema", "Cache limpo!", 2000, "success")

ModernButton(monitor_tab, "Limpar Cache", menu,
             callback=lambda: threading.Thread(target=clear_cache, daemon=True).start(),
             button_style="warning")

ModernButton(monitor_tab, "Parar Monitoramento", menu,
             callback=lambda: running.update({'value': False}),
             button_style="danger")

menu.run()
```

### 6.2 Ferramenta de Aimbot Visual Completa

```python
from cliv_gui import ClivMenu, ProcessOverlay, ModernSlider, ModernCheck, DynamicColorPicker
import threading
import time

# Menu de configuração
menu = ClivMenu(title="AIMBOT CONFIG", theme_color="#e74c3c")
config_tab = menu.add_tab("CONFIG")
visuals_tab = menu.add_tab("VISUAL")

# Configurações principais
fov_slider = ModernSlider(config_tab, "FOV Circle", 1, 500, menu, default=120)
smooth_slider = ModernSlider(config_tab, "Suavização", 1, 20, menu, default=5)
aimbot_check = ModernCheck(config_tab, "Aimbot Ativado", menu, default=False)
esp_check = ModernCheck(visuals_tab, "ESP Ativado", menu, default=True)

# Color picker para FOV
fov_color_picker = DynamicColorPicker(visuals_tab, "FOV_COLOR", menu)
esp_color_picker = DynamicColorPicker(visuals_tab, "ESP_COLOR", menu)

# Overlay
overlay = ProcessOverlay("game.exe", alpha=0.3)

running = {'value': True}

def draw_loop():
    while running['value']:
        overlay.clear_drawings()

        # Obter configurações
        fov = fov_slider.get_value()
        aimbot_enabled = aimbot_check.get_value()
        esp_enabled = esp_check.get_value()
        fov_color = menu.data.get("FOV_COLOR", "#00ff00")
        esp_color = menu.data.get("ESP_COLOR", "#ff0000")

        if aimbot_enabled:
            # Desenhar FOV circle
            overlay.draw_circle(960, 540, fov, fov_color, 2)

            # Crosshair
            overlay.draw_crosshair(960, 540, 20, "red", 2)

            # Status
            overlay.draw_text(20, 20, "AIMBOT: ON", "lime",
                            ("Arial", 14, "bold"))

        if esp_enabled:
            # Aqui você implementaria a detecção de players
            # Exemplo com dados mock:
            mock_players = [
                {"x": 300, "y": 200, "name": "Enemy", "health": 75},
                {"x": 600, "y": 350, "name": "Enemy2", "health": 50},
            ]

            for player in mock_players:
                x, y = player["x"], player["y"]
                health = player["health"]

                # Box ESP
                overlay.draw_rectangle(x-30, y-60, 60, 120, esp_color, 2)

                # Nome
                overlay.draw_text(x, y-75, player["name"], esp_color,
                                ("Arial", 10, "bold"))

                # Health bar
                health_width = int(60 * (health / 100))
                bar_color = "lime" if health > 50 else "yellow" if health > 25 else "red"
                overlay.draw_rectangle(x-30, y-80, health_width, 4,
                                     bar_color, 0, fill=bar_color)

        time.sleep(0.016)  # ~60 FPS

# Iniciar overlay em thread
def start_overlay():
    if overlay.start():
        menu.show_notification("Overlay", "Iniciado com sucesso!", 2000, "success")
        threading.Thread(target=draw_loop, daemon=True).start()
    else:
        menu.show_notification("Erro", "Processo não encontrado!", 3000, "error")

menu.root.after(1000, start_overlay)

# Cleanup ao fechar
def on_close():
    running['value'] = False
    overlay.stop()
    menu._on_close()

menu._on_close = on_close

# Iniciar menu
menu.run("f1")
```

### 6.3 Player de Música com Visualizador

```python
from cliv_gui import ClivMenu, AudioPlayer, ModernGraph, ModernButton
import random
import threading
import time

menu = ClivMenu(title="MUSIC PLAYER", theme_color="#9b59b6", width=500)
player_tab = menu.add_tab("PLAYER")

# Player de áudio
audio = AudioPlayer(player_tab, menu, "music.mp3", autoplay=False, loop=True)

# Visualizador
visualizer = ModernGraph(player_tab, "AUDIO VISUALIZER", menu, max_values=100)

running = {'value': True}

# Simular visualização de áudio
def update_visualizer():
    while running['value']:
        status = audio.get_status()

        if status['playing']:
            # Simular amplitude de áudio (você pode integrar análise real)
            amplitude = random.randint(20, 100)
            visualizer.add_value(amplitude)
        else:
            visualizer.add_value(0)

        time.sleep(0.05)  # 20 Hz

# Iniciar visualizador
threading.Thread(target=update_visualizer, daemon=True).start()

# Controles adicionais
def change_song():
    # Aqui você implementaria um file picker
    audio.set_audio_file("outro.mp3")
    menu.show_notification("Player", "Música alterada", 2000, "info")

ModernButton(player_tab, "Trocar Música", menu,
             callback=change_song, button_style="info")

# Cleanup
def on_close():
    running['value'] = False
    audio.stop_music()
    menu._on_close()

menu._on_close = on_close

menu.run()
```

### 6.4 Trainer de Jogo Completo

```python
from cliv_gui import (ClivMenu, ModernButton, ModernCheck,
                      ModernSlider, KeyBind, ImageSeparator,
                      DynamicColorPicker)

menu = ClivMenu(title="GAME TRAINER", theme_color="#e74c3c", width=500, height=750)

# ===== ABA: CHEATS =====
cheats_tab = menu.add_tab("CHEATS")

ImageSeparator(cheats_tab, "PLAYER CHEATS", menu_ref=menu)

godmode_check = ModernCheck(cheats_tab, "God Mode", menu, default=False,
                            callback=lambda v: activate_godmode(v))
ammo_check = ModernCheck(cheats_tab, "Infinite Ammo", menu, default=False)
noclip_check = ModernCheck(cheats_tab, "No Clip", menu, default=False)

ImageSeparator(cheats_tab, "VISUAL CHEATS", menu_ref=menu)

esp_players = ModernCheck(cheats_tab, "ESP Players", menu, default=False)
esp_items = ModernCheck(cheats_tab, "ESP Items", menu, default=False)
esp_health = ModernCheck(cheats_tab, "ESP Health Bars", menu, default=False)

# ===== ABA: CONFIGURAÇÕES =====
config_tab = menu.add_tab("CONFIG")

ImageSeparator(config_tab, "GAMEPLAY", menu_ref=menu)

speed_slider = ModernSlider(config_tab, "Speed Multiplier", 1, 10, menu, default=1)
jump_slider = ModernSlider(config_tab, "Jump Height", 1, 100, menu, default=10)
fov_slider = ModernSlider(config_tab, "FOV", 60, 120, menu, default=90)

ImageSeparator(config_tab, "VISUAL", menu_ref=menu)

esp_color = DynamicColorPicker(config_tab, "ESP_COLOR", menu)
crosshair_color = DynamicColorPicker(config_tab, "CROSSHAIR_COLOR", menu)

# ===== ABA: HOTKEYS =====
hotkey_tab = menu.add_tab("HOTKEYS")

ImageSeparator(hotkey_tab, "KEYBINDS", menu_ref=menu)

god_key = KeyBind(hotkey_tab, "God Mode Key", "GOD_KEY", menu, default="F1")
esp_key = KeyBind(hotkey_tab, "ESP Key", "ESP_KEY", menu, default="F2")
speed_key = KeyBind(hotkey_tab, "Speed Key", "SPEED_KEY", menu, default="F3")
noclip_key = KeyBind(hotkey_tab, "NoClip Key", "NOCLIP_KEY", menu, default="F4")

# ===== ABA: INFO =====
info_tab = menu.add_tab("INFO")

ImageSeparator(info_tab, "ABOUT", menu_ref=menu)

def check_updates():
    menu.show_notification("Update", "Verificando atualizações...", 2000, "info")
    # Implementar verificação
    menu.root.after(2000, lambda: menu.show_notification(
        "Update", "Você está atualizado!", 2000, "success"))

def open_discord():
    import webbrowser
    webbrowser.open("https://discord.gg/example")
    menu.show_notification("Discord", "Abrindo servidor...", 2000, "info")

ModernButton(info_tab, "Check for Updates", menu,
             callback=check_updates, button_style="info")

ModernButton(info_tab, "Discord Server", menu,
             callback=open_discord, button_style="primary")

# Funções de ativação (implementar conforme necessário)
def activate_godmode(enabled):
    if enabled:
        menu.show_notification("God Mode", "Ativado!", 2000, "success")
    else:
        menu.show_notification("God Mode", "Desativado", 2000, "info")

menu.run("insert")
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
pip install pygame --upgrade --force-reinstall
```

#### Erro: "ImportError: DLL load failed"

**Causa:** pywin32 não instalado corretamente

**Solução:**
```bash
pip uninstall pywin32
pip install pywin32==304
# No Windows, execute também:
python C:\Python3X\Scripts\pywin32_postinstall.py -install
```

#### Erro: "RuntimeError: Tabs não estão habilitadas"

**Causa:** Tentou usar `add_tab()` quando `enable_tabs=False`

**Solução:**
```python
# Opção 1: Habilitar tabs
menu = ClivMenu(enable_tabs=True)

# Opção 2: Usar get_container()
menu = ClivMenu(enable_tabs=False)
container = menu.get_container()
```

#### Overlay não aparece

**Checklist:**
1. ✅ Processo está rodando?
2. ✅ Nome do processo está correto? (verificar no Task Manager)
3. ✅ Executando como administrador?
4. ✅ Janela do jogo está visível (não minimizada)?
5. ✅ Jogo não está em fullscreen exclusivo (usar borderless windowed)?

**Solução:**
```python
# Verificar se processo existe
import psutil

def check_process(name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == name.lower():
            print(f"✓ Processo encontrado: PID {proc.pid}")
            return True
    print(f"✗ Processo '{name}' não encontrado!")
    return False

check_process("notepad.exe")
```

#### Notificações não aparecem

**Causa:** Outras janelas cobrindo ou múltiplos monitores

**Solução:**
Ajustar posição manualmente no código:
```python
# Editar NotificationManager._animate_in() se necessário
# Linha ~45-50 do código
x = screen_width - width - 20  # Ajuste X
y = screen_height - height - 60 - offset  # Ajuste Y
```

#### Menu não responde à hotkey

**Causa:** Permissões insuficientes ou conflito de tecla

**Solução:**
```python
# 1. Executar como administrador
# 2. Ou usar tecla diferente
menu.run("f10")  # Ao invés de INSERT

# 3. Verificar se keyboard está funcionando
import keyboard
keyboard.add_hotkey("f10", lambda: print("Tecla funcionando!"))
```

### 7.2 Debug Mode

Para debug detalhado, ative logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Agora todas as operações internas serão logadas
```

### 7.3 Performance

Se o menu estiver lento:

```python
# 1. Reduzir partículas
menu = ClivMenu(part_count=10)  # Menos partículas

# 2. Desabilitar partículas completamente
menu = ClivMenu(part_count=0)

# 3. Reduzir FPS do overlay
# Em draw_loop(), aumentar sleep:
time.sleep(0.033)  # 30 FPS ao invés de 60

# 4. Reduzir taxa de atualização de gráficos
# Atualizar a cada 2 segundos ao invés de 1:
menu.root.after(2000, update_stats)
```

---

## 8. Best Practices

### 8.1 Estrutura de Código

```python
# ✅ BOM - Organizado em classe
class MyApp:
    def __init__(self):
        self.menu = ClivMenu(title="MY APP", enable_tabs=True)
        self.running = True
        self.setup_ui()

    def setup_ui(self):
        self.create_tabs()
        self.add_components()
        self.bind_callbacks()

    def create_tabs(self):
        self.main_tab = self.menu.add_tab("MAIN")
        self.config_tab = self.menu.add_tab("CONFIG")

    def add_components(self):
        self.start_btn = ModernButton(
            self.main_tab, "Start", self.menu,
            callback=self.on_start, button_style="success"
        )

        self.config_slider = ModernSlider(
            self.config_tab, "Value", 0, 100, self.menu,
            default=50, callback=self.on_value_change
        )

    def bind_callbacks(self):
        # Configurar cleanup ao fechar
        original_close = self.menu._on_close
        def cleanup():
            self.running = False
            # Parar threads, salvar configs, etc.
            original_close()
        self.menu._on_close = cleanup

    def on_start(self):
        self.menu.show_notification("App", "Iniciado!", 2000, "success")

    def on_value_change(self, value):
        print(f"Valor alterado: {value}")

    def run(self):
        self.menu.run("insert")

# Uso
app = MyApp()
app.run()
```

```python
# ❌ RUIM - Desorganizado
menu = ClivMenu(title="MY APP")
tab1 = menu.add_tab("MAIN")
ModernButton(tab1, "Start", menu, callback=lambda: print("Started!"))
tab2 = menu.add_tab("CONFIG")
# ... código espalhado sem estrutura
menu.run()
```

### 8.2 Gerenciamento de Estado

```python
# ✅ BOM - Usar menu.data como estado central
menu.data['esp_enabled'] = True
menu.data['fov'] = 120
menu.data['config'] = {
    'graphics': 'high',
    'resolution': '1920x1080'
}

# Acessar de callbacks
def toggle_esp(checked):
    menu.data['esp_enabled'] = checked
    update_esp()
    save_config()

def get_config():
    return menu.data.get('config', {})
```

```python
# ❌ RUIM - Variáveis globais
esp_enabled = True
fov = 120

def toggle_esp(checked):
    global esp_enabled
    esp_enabled = checked
    # Difícil de rastrear e manter
```

### 8.3 Threading Seguro

```python
# ✅ BOM - Daemon threads com flag de controle
class MyApp:
    def __init__(self):
        self.running = {'value': True}

    def background_task(self):
        while self.running['value']:
            do_something()
            time.sleep(1)

    def start_background(self):
        thread = threading.Thread(target=self.background_task, daemon=True)
        thread.start()

    def stop(self):
        self.running['value'] = False
```

```python
# ❌ RUIM - Thread sem daemon e sem controle
def background_task():
    while True:  # Nunca para!
        do_something()
        time.sleep(1)

thread = threading.Thread(target=background_task)
thread.start()
# Thread continua rodando após fechar menu!
```

### 8.4 Tratamento de Erros

```python
# ✅ BOM - Try/except com notificações
def safe_operation():
    try:
        result = risky_function()
        menu.show_notification("Sucesso", "Operação OK!", 2000, "success")
        return result
    except FileNotFoundError as e:
        menu.show_notification("Erro", "Arquivo não encontrado", 3000, "error")
        logging.error(f"FileNotFoundError: {e}")
    except Exception as e:
        menu.show_notification("Erro", f"Erro inesperado: {e}", 3000, "error")
        logging.exception("Erro em safe_operation")
    return None
```

```python
# ❌ RUIM - Sem tratamento
def unsafe_operation():
    result = risky_function()  # Pode crashar todo o programa!
    return result
```

### 8.5 Limpeza de Recursos

```python
# ✅ BOM - Cleanup completo ao fechar
class MyApp:
    def __init__(self):
        self.menu = ClivMenu()
        self.overlay = ProcessOverlay("game.exe")
        self.threads_running = True

        # Sobrescrever método de fechamento
        original_close = self.menu._on_close
        def cleanup():
            self.cleanup_resources()
            original_close()
        self.menu._on_close = cleanup

    def cleanup_resources(self):
        # Parar threads
        self.threads_running = False

        # Parar overlay
        if hasattr(self, 'overlay'):
            self.overlay.stop()

        # Salvar configurações
        self.save_config()

        # Parar áudio
        if hasattr(self, 'audio_player'):
            self.audio_player.stop_music()

    def save_config(self):
        try:
            with open('config.json', 'w') as f:
                json.dump(self.menu.data, f, indent=2)
        except Exception as e:
            logging.error(f"Erro ao salvar config: {e}")
```

### 8.6 Uso de WidgetStyle

```python
# ✅ BOM - Estilos reutilizáveis
class MyApp:
    def __init__(self):
        self.menu = ClivMenu()

        # Definir estilos uma vez
        self.header_style = WidgetStyle(
            font=("Arial", 12, "bold"),
            margin=(15, 10, 5, 10),
            bg_color=self.menu.bg_color
        )

        self.button_style = WidgetStyle(
            padding=(15, 15, 15, 15),
            margin=(10, 10, 10, 10)
        )

    def create_ui(self):
        tab = self.menu.add_tab("MAIN")

        # Usar estilos consistentes
        ImageSeparator(tab, "SECTION 1", menu_ref=self.menu,
                      style=self.header_style)
        ModernButton(tab, "Action", self.menu, style=self.button_style)
```

```python
# ❌ RUIM - Estilos inconsistentes
# Cada widget com configuração diferente, difícil de manter
ModernButton(tab, "Btn1", menu, style=WidgetStyle(padding=(10,10,10,10)))
ModernButton(tab, "Btn2", menu, style=WidgetStyle(padding=(12,12,12,12)))
ModernButton(tab, "Btn3", menu, style=WidgetStyle(padding=(8,8,8,8)))
```

---

## 9. FAQ

### 9.1 Geral

**P: ClivGui funciona em Linux/Mac?**
R: Não, é exclusivo para Windows devido ao uso extensivo de APIs do Windows (pywin32, win32gui, etc.).

**P: Posso usar para aplicações comerciais?**
R: Sim! A licença MIT permite uso comercial sem restrições.

**P: Como compilar para .exe?**
R: Use PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --icon=icon.ico meu_app.py
```

Para overlay, inclua dados:
```bash
pyinstaller --onefile --noconsole --add-data "assets;assets" meu_app.py
```

**P: Qual a diferença entre ClivMenu e ProcessOverlay?**
R: ClivMenu é o menu de configuração (GUI). ProcessOverlay é o overlay transparente sobre jogos/apps. Normalmente você usa ambos juntos.

**P: Preciso usar abas?**
R: Não! Use `enable_tabs=False` para aplicações simples:
```python
menu = ClivMenu(enable_tabs=False)
container = menu.get_container()
```

### 9.2 Técnicas

**P: Como fazer o overlay seguir um objeto específico?**
R: Atualize as coordenadas em tempo real:
```python
def track_object():
    while True:
        x, y = get_object_position()  # Sua função de detecção
        overlay.clear_drawings()
        overlay.draw_circle(x, y, 50, "red", 2)
        time.sleep(0.016)
```

**P: Como salvar configurações automaticamente?**
R: Use `menu.data` e salve no fechamento:
```python
def save_on_close():
    with open('config.json', 'w') as f:
        json.dump(menu.data, f)
    menu._on_close()

menu._on_close = save_on_close
```

**P: Como adicionar ícone customizado ao menu?**
R: Defina o ícone da janela:
```python
try:
    menu.root.iconbitmap('icon.ico')
except:
    pass  # Ícone não encontrado
```

**P: Como mudar tema dinamicamente?**
R: Atualize a cor do tema:
```python
menu.theme = "#e74c3c"
# Componentes criados DEPOIS usarão a nova cor
```

**P: Como integrar com detecção de jogos real?**
R: Você precisa implementar a lógica de leitura de memória/detecção. ClivGui fornece apenas a interface e overlay visual. Exemplos:
- Usar bibliotecas como `pymem` para leitura de memória
- Usar OpenCV para detecção de imagem
- Usar APIs do jogo se disponíveis

### 9.3 Troubleshooting

**P: Por que o menu não aparece?**
R: Verifique se está chamando `menu.run()` e se não há erros no console. Execute com logging ativado.

**P: Hotkey não funciona?**
R: Execute como administrador ou use uma tecla diferente. Algumas teclas podem estar bloqueadas ou em uso por outros programas.

**P: Overlay aparece atrás da janela do jogo?**
R: Certifique-se que o jogo não está em fullscreen exclusivo. Use borderless windowed mode.

**P: Notificações sobrepõem outras janelas?**
R: É o comportamento esperado (topmost). Elas são projetadas para serem sempre visíveis.

**P: Como desabilitar partículas?**
R: Use `part_count=0`:
```python
menu = ClivMenu(part_count=0)
```

**P: ProcessOverlay consome muita CPU?**
R: Reduza o FPS aumentando o sleep no loop:
```python
time.sleep(0.033)  # 30 FPS ao invés de 60
```

---

## 📚 Recursos Adicionais

- **GitHub:** https://github.com/Night613/ClivGui
- **Exemplos:** https://github.com/Night613/ClivGui/tree/main/examples
- **Issues:** https://github.com/Night613/ClivGui/issues
- **Contato:** clivguicontact@gmail.com

---

## 📄 Licença

ClivGui é licenciado sob a MIT License.

Copyright © 2026 Night613

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**Última atualização:** 08/02/2026
**Versão da documentação:** 1.0.4
