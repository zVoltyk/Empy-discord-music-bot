import os
import subprocess
from dotenv import load_dotenv
import discord as ds
from discord.ext import commands
import yt_dlp
import asyncio

intents = ds.Intents.default()
intents.message_content = True
intents.members = True
empy = commands.Bot(command_prefix='!', intents=intents)

song_queue = {}
ffmpeg_global_path = "ffmpeg"
ffmpeg_local_path = os.path.join(os.getcwd(), "ffmpeg-master-latest-win64-gpl-shared", "bin", "ffmpeg.exe")

#ffmpeg path check
def check_ffmpeg_path():
    try:
        #check if ffmpeg is in the system PATH
        subprocess.check_output(["where", ffmpeg_global_path], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        #if it isn't, check if ffmpeg is in the local path
        if os.path.isfile(ffmpeg_local_path):
            return True
        return False

#yt-dlp config
def get_audio_info(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        #playlist
        if 'entries' in info:
            return [
                {
                    'url': entry['url'],
                    'title': entry.get('title', 'Audio')
                } for entry in info['entries'] if entry.get('url')
            ]
        else:
            return [{
                'url': info['url'],
                'title': info.get('title', 'Audio')
            }]

#verificacion inicio correcto a discord
@empy.event
async def on_ready():
    print(f'{empy.user} inició sesión (⌐■_■)')

#join channel
@empy.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Me uní a {channel} (ɔ◔‿◔)ɔ')
    else:
        await ctx.send('No hay nadie conectado ヾ(≧へ≦)〃')

#play next song in queue
async def play_next(ctx):
    guild_id = ctx.guild.id
    voice_client = ctx.guild.voice_client

    if song_queue.get(guild_id) and song_queue[guild_id]:
        next_song = song_queue[guild_id].pop(0)

        if not check_ffmpeg_path():
            print("Error: No se pudo encontrar FFmpeg. Por favor asegúrate de que FFmpeg esté instalado en el PATH global o en el directorio raíz del programa.")

        source = ds.FFmpegPCMAudio(
            next_song['url'],
            executable="ffmpeg", # if you don't have ffmpeg in your PATH, use the full path to the executable like "C:/Users/user/Desktop/bot-folder/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe"
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn"
        )
    
        def after_playing(err):
            if err:
                print(f"Error en reproducción: {err}")
            
            fut = asyncio.run_coroutine_threadsafe(play_next(ctx), empy.loop)

            try:
                fut.result()
            except Exception as e:
                print(f"Error post-reproduccion: {e}")
        
        voice_client.play(source, after=after_playing)
        await ctx.send(f'🎶 Preparada para cantar \(＾▽＾)/:\n* **{next_song["title"]}**')

#play song
@empy.command()
async def play(ctx, *, url):
    guild_id = ctx.guild.id
    
    if guild_id not in song_queue:
        song_queue[guild_id] = []

    if not ctx.voice_client:
        await ctx.invoke(join)

    try:
        infos = get_audio_info(url)
        song_queue[guild_id].extend(infos)
        await ctx.send(f'✅ Añadido(s) a la cola (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧:\n' + '\n'.join([f'* **{i["title"]}**' for i in infos]))

        if not ctx.voice_client.is_playing():
            await play_next(ctx)
    except Exception as e:
        await ctx.send(f'Ocurrio un error: {e} ヾ(≧へ≦)〃')

#pause song
@empy.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send('▶️ Reproducción pausada (－‸ლ)')
        # replace if the code above doesn't display properly
        # await ctx.send(':pause_button: Reproducción pausada (－‸ლ)')
    else:
        await ctx.send('No se está reproduciendo nada para pausar (・_・;)')

#resume song
@empy.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send('⏸️ Reproducción reanudada (｀・ω・)ゞ')
        # replace if the code above doesn't display properly
        # await ctx.send(':arrow_forward: Reproducción reanudada (｀・ω・)ゞ')
    else:
        await ctx.send('No hay nada pausado para reanudar (・_・;)')

#skip song
@empy.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('⏭️ Canción omitida (￣︶￣)/')
        # replace if the code above doesn't display properly
        # await ctx.send(':track_next: Canción omitida (￣︶￣)/')
    else:
        await ctx.send('No se está reproduciendo nada para omitir (・_・;)')

#leave channel
@empy.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('💤 Adiosito (_ _) 。z Z')
    else:
        await ctx.send('💤 Déjenme dormir (￣o￣) 。z Z')

#show queue
@empy.command()
async def queue(ctx):
    guild_id = ctx.guild.id
    
    if song_queue.get(guild_id):
        msg = '\n'.join([f"{idx+1}. {song['* title']}" for idx, song in enumerate(song_queue[guild_id])])
        await ctx.send(f'📜 Lista actual (￣︶￣)/:\n{msg}')
    else:
        await ctx.send('La lista está vacía (≧◇≦)')

#clear queue
@empy.command()
async def clearqueue(ctx):
    guild_id = ctx.guild.id
    
    if song_queue.get(guild_id):
        song_queue[guild_id] = []
        await ctx.send("🗑️ Lista limpiada (￣︶￣)/")
    else:
        await ctx.send("No hay canciones en la lista para limpiar (・_・;)")

#remove from queue
@empy.command()
async def remove(ctx, index: int):
    guild_id = ctx.guild.id
    
    if song_queue.get(guild_id):
        if 0 < index <= len(song_queue[guild_id]):
            removed = song_queue[guild_id].pop(index - 1)
            await ctx.send(f"❌ Eliminada (｡• ︵•｡):\n* **{removed['title']}** de la lista.")
        else:
            await ctx.send("Ese número no corresponde a ninguna canción de la lista ヾ(≧へ≦)〃")
    else:
        await ctx.send("La lista está vacía (・_・;)")

#read token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

empy.run(TOKEN)