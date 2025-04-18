# 🎧 Empy Discord Music Bot (Python)

Un bot de música simple y adorable para Discord usando `discord.py` y `yt-dlp`.  
¡Soporta colas, playlists, pausar/reanudar y más!  
Cada mensaje del bot incluye un kaomoji único para hacerlo más divertido~ (＾▽＾)

---

# 📦 Funciones

- ✅ Unirse y salir de canales de voz
- 🎵 Reproducir canciones y playlists de YouTube
- ⏯️ Pausar / reanudar
- ⏩ Saltar canción actual
- 🗑️ Limpiar o eliminar de la cola
- 📜 Mostrar la cola actual
- 💌 Kaomojis lindos en cada respuesta

---

# 🔧 Requisitos

- Python 3.9 o superior
- [FFmpeg](https://ffmpeg.org/download.html)
- Un token de bot de Discord

---

# 🚀 Instalación

1. **Clona este repositorio**
```bash
git clone https://github.com/tu-usuario/tu-repo-privado.git
cd tu-repo-privado
```

2. **Crea y activa un entorno virtual (opcional, pero recomendado)**
```bash
python -m venv venv
venv\Scripts\activate    # En Windows
# o
source venv/bin/activate # En macOS/Linux
```

3. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

4. **Crea un archivo .env en la raíz del proyecto y añade tu token de bot:**
```ini
DISCORD_TOKEN='TU_TOKEN_DEL_BOT'
```

# 🎥 Configuración de FFmpeg

Este proyecto usa FFmpeg para reproducir audio.

## Opción 1: Usar FFmpeg portable (recomendado para uso local)

1. Descarga la última versión para Windows desde [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
2. Extrae la carpeta (por ejemplo, ffmpeg-master-latest-win64-gpl-shared/) dentro del proyecto.
3. El bot ya está configurado para usar el ffmpeg.exe dentro de esa carpeta.

```vbnet
ffmpeg-master-latest-win64-gpl-shared/
```

## Opción 2: Agrega FFmpeg al PATH del sistema

Agrega la carpeta bin/ dentro de FFmpeg a las variables de entorno (PATH) de tu sistema para que ffmpeg sea accesible globalmente.

# 🐣 Ejecutar el bot
```bash
python bot.py
```

# ✨ Comandos de ejemplo
```diff
!join
!play <url>
!pause
!resume
!skip
!queue
!remove <index>
!clearqueue
!leave
```

# 💖 Créditos
Hecho con amor usando:

- discord.py

- yt-dlp

- FFmpeg

# 📬 Colaboraciones

Este proyecto es público para todos para disfrutar y aprender~ 🎶

No acepto contribuciones directas sin consultarlo previamente.

Si quieres sugerir algún cambio o trabajar juntos, no dudes en contactarme (｡•̀ᴗ-)✧

## Que comience la música~ ♪ヽ(･ˇ∀ˇ･ゞ)