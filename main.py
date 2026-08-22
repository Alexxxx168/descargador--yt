from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Asegurarnos de que la carpeta descargas exista
if not os.path.exists('descargas'):
    os.makedirs('descargas')

@app.route('/')
def inicio():
    # Muestra la página web al entrar
    return render_template('index.html')

@app.route('/descargar', methods=['POST'])
def descargar_video():
    url = request.form.get('url')
    opcion = request.form.get('formato')
    
    # Guardaremos el archivo usando el ID del video para evitar errores con caracteres raros
    ydl_opts = {
        'outtmpl': 'descargas/%(id)s.%(ext)s'
    }

    if opcion == "1":
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        })
        ext_final = '.mp4'
    else:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
        ext_final = '.mp3'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraemos la información y descargamos
            info = ydl.extract_info(url, download=True)
            video_id = info['id']
            titulo = info['title']
            
            # Ruta del archivo descargado
            ruta_archivo = f"descargas/{video_id}{ext_final}"
            
            # Enviamos el archivo al navegador del usuario
            return send_file(
                ruta_archivo, 
                as_attachment=True, 
                download_name=f"{titulo}{ext_final}" # El usuario lo descarga con el nombre real
            )
    except Exception as e:
        return f"Ocurrió un error durante la descarga: {str(e)}"

if __name__ == '__main__':
    # Inicia el servidor web local
    app.run(debug=True)