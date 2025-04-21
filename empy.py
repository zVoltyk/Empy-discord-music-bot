import discord as ds
from discord.ext import commands
from discord import app_commands
import subprocess
import asyncio
import yt_dlp
import os
from keep_alive import keep_alive
from dotenv import load_dotenv

intents = ds.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
empy = commands.Bot(command_prefix='!', intents=intents)
tree = empy.tree

song_queue = {}
ffmpeg_global_path = "ffmpeg"
ffmpeg_local_path = os.path.join(os.getcwd(), "ffmpeg-master-latest-win64-gpl-shared", "bin", "ffmpeg.exe")

#read token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

#bot discord login verification
@empy.event
async def on_ready():
    guild = ds.Object(id=GUILD_ID)
    await tree.sync(guild=guild)
    print(f'{empy.user} inició sesión (⌐■_■)')

#ffmpeg path check
def check_ffmpeg_path():
    try:
        #check if ffmpeg is in the system PATH
        subprocess.check_output(["where", ffmpeg_global_path], stderr=subprocess.DEVNULL)
        return ffmpeg_global_path
    except subprocess.CalledProcessError:
        #if it isn't, check if ffmpeg is in the local path
        return ffmpeg_local_path if os.path.isfile(ffmpeg_local_path) else None

#YouTube info extraction
def get_audio_info(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        #playlist
        if 'entries' in info:
            return [
                {
                    'url': entry.get('url') or entry.get('webpage_url'),
                    'title': entry.get('title', 'Audio')
                } for entry in info['entries']
            ]
        else:
            return [{
                'url': info.get('url') or info.get('webpage_url'),
                'title': info.get('title', 'Audio')
            }]

#play next song in queue
async def play_next(interaction):
    guild_id = interaction.guild.id
    voice_client = interaction.guild.voice_client

    if song_queue.get(guild_id) and song_queue[guild_id]:
        next_song = song_queue[guild_id].pop(0)
        
        ffmpeg_exec = check_ffmpeg_path()
        try:
            source = ds.FFmpegPCMAudio(
                next_song['url'],
                executable=ffmpeg_exec, # if you don't have ffmpeg in your PATH, use the full path to the executable like "C:/Users/user/Desktop/bot-folder/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe"
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                options="-vn"
            )
        
            def after_playing(err):                
                fut = asyncio.run_coroutine_threadsafe(play_next(interaction), empy.loop)

                try:
                    fut.result()
                except Exception as e:
                    print(f"Error al continuar: {e}")
            
            voice_client.play(source, after=after_playing)
            embed = ds.Embed(title="🎶 Preparada para cantar (＾▽＾)/:\n", description=f"**{next_song['title']}**", color=0x1DB954)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.send(f"No se pudo reproducir la canción (・_・;):\n{e}")
            await play_next(interaction)

# === SLASH COMMANDS ===

#join channel
@tree.command(name="join", description="Unirse a un canal de voz")
async def join(interaction: ds.Interaction):
    await interaction.response.defer()
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.followup.send(f"Me uní a {channel} (ɔ◔‿◔)ɔ")
    else:
        await interaction.followup.send("No hay nadie conectado ヾ(≧へ≦)〃")

#play song
@tree.command(name="play", description="Reproducir una canción por URL")
@app_commands.describe(url="Link de YouTube o playlist")
async def play(interaction: ds.Interaction, url: str):
    await interaction.response.defer()
    guild_id = interaction.guild.id
    
    if guild_id not in song_queue:
        song_queue[guild_id] = []

    voice_client = interaction.guild.voice_client
    if not voice_client:
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice_client = await channel.connect()
        else:
            await interaction.followup.send("No hay nadie conectado ヾ(≧へ≦)〃")
            return

    try:
        infos = get_audio_info(url)
        song_queue[guild_id].extend(infos)

        embed = ds.Embed(title="🎶 Añadido(s) a la cola (ﾉ◕ヮ◕)ﾉ*･ﾟ✧:\n", color=0x3498db) 
        for i in infos:
            embed.add_field(name="", value=i["title"], inline=False)
        await interaction.followup.send(embed=embed)

        if not interaction.guild.voice_client.is_playing():
            await play_next(interaction)
    except Exception as e:
        await interaction.followup.send(f"Ocurrio un error: {e} ヾ(≧へ≦)〃")

#show queue
@tree.command(name="queue", description="Mostrar la lista de canciones")
async def queue(interaction: ds.Interaction):
    await interaction.response.defer()
    queue_list = song_queue.get(interaction.guild.id, [])
    
    if not queue_list:
        await interaction.followup.send("🎧 La lista está vacía (≧◇≦)")
        return
    
    embed = ds.Embed(title="📜 Lista actual (￣︶￣)/:\n", color=0xFFC300)
    for idx, song in enumerate(queue_list):
        embed.add_field(name=f"{idx+1}.", value=song["title"], inline=False)
    await interaction.followup.send(embed=embed)

#pause song
@tree.command(name="pause", description="Pausar la canción actual")
async def pause(interaction: ds.Interaction):
    await interaction.response.defer()
    if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.pause()
        await interaction.followup.send("▶️ Reproducción pausada (－‸ლ)")
        # replace if the code above doesn't display properly
        # await interaction.followup.send(':pause_button: Reproducción pausada (－‸ლ)')
    else:
        await interaction.send("No se está reproduciendo nada para pausar (・_・;)")

#resume song
@tree.command(name="resume", description="Reanudar la canción actual")
async def resume(interaction: ds.Interaction):
    await interaction.response.defer()
    if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
        interaction.guild.voice_client.resume()
        await interaction.followup.send("⏸️ Reproducción reanudada (｀・ω・)ゞ")
        # replace if the code above doesn't display properly
        # await interaction.followup.send(':arrow_forward: Reproducción reanudada (｀・ω・)ゞ')
    else:
        await interaction.followup.send("No hay nada pausado para reanudar (・_・;)")

#skip song
@tree.command(name="skip", description="Omitir la canción actual")
async def skip(interaction: ds.Interaction):
    await interaction.response.defer()
    if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.stop()
        await interaction.followup.send("⏭️ Canción omitida (￣︶￣)/")
        # replace if the code above doesn't display properly
        # await interaction.followup.send(':track_next: Canción omitida (￣︶￣)/')
    else:
        await interaction.followup.send("No se está reproduciendo nada para omitir (・_・;)")

#leave channel
@tree.command(name="leave", description="Desconectarse del canal de voz")
async def leave(interaction: ds.Interaction):
    await interaction.response.defer()
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.followup.send("💤 Adiosito (_ _) 。z Z")
    else:
        await interaction.followup.send("💤 Déjenme dormir (￣o￣) 。z Z")

#clear queue
@tree.command(name="clearqueue", description="Limpiar la lista de canciones")
async def clearqueue(interaction: ds.Interaction):
    await interaction.response.defer()
    guild_id = interaction.guild.id
    
    if song_queue.get(guild_id):
        song_queue[guild_id] = []
        await interaction.followup.send(embed=ds.Embed(
            title="🗑️ Lista limpiada (￣︶￣)/",
            description="La lista de canciones ha sido limpiada (￣︶￣)/",
            color=0xFF5733
        ))
    else:
        await interaction.followup.send("No hay canciones en la lista para limpiar (・_・;)")

#remove from queue
@tree.command(name="remove", description="Eliminar una canción de la lista")
@app_commands.describe(index="Número de la canción a eliminar (desde 1)")
async def remove(interaction: ds.Interaction, index: int):
    await interaction.response.defer()
    guild_id = interaction.guild.id
    queue_list = song_queue.get(guild_id)
    
    if queue_list:
        if 0 < index <= len(queue_list):
            removed = queue_list.pop(index - 1)
            await interaction.followup.send(embed=ds.Embed(
                title="🗑️ Eliminada (￣︶￣)/",
                description=f"**{removed['title']}** ha sido eliminada de la lista (￣︶￣)/",
                color=0xC70039
            ))
        else:
            await interaction.followup.send("Ese número no corresponde a ninguna canción de la lista ヾ(≧へ≦)〃")
    else:
        await interaction.followup.send("La lista está vacía (・_・;)")

empy.run(TOKEN)