from flask import Flask, render_template, request
import subprocess
import threading
import os

app = Flask(__name__)

def process_text(text, quality):
    start_index = text.find("https://d1d34p8vz63oiq.cloudfront.net")
    end_index = text.find("/dash/")
    url = text[start_index:end_index]
 
    final_url = url.replace("d1d34p8vz63oiq", "d26g5bnklkwsh4")

    final_url = final_url.split("dash")[0] + "/hls/{}/main.m3u8".format(quality)
 
    return final_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get quality from the input form
        quality = request.form['quality']
        # Get the input text from the form
        input_text_value = request.form['link']
        # Get the desired file name from the form
        file_name = request.form['file_name']

        # Process the input text
        final_link = process_text(input_text_value, quality)

        # Construct the yt-dlp command with the desired file name and download directory
        command = f'yt-dlp -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best -o "D:\Physicswallah/{file_name}.%(ext)s" --hls-prefer-native -N 8 "{final_link}"'

        print("Download started!")

        try:
            # Execute the download command using subprocess asynchronously
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr with stdout to capture all logs
                universal_newlines=True
            )

            # Start a thread to wait for the download process to complete
            threading.Thread(target=wait_for_download, args=(process,)).start()

            return 'Download started!'

        except subprocess.CalledProcessError as e:
            error_message = f"Download failed with error:\n\n{e.output}"
            print(error_message)
            return error_message

    return render_template('index.html')

def wait_for_download(process):
    for line in iter(process.stdout.readline, ''):
        print(line.strip())  # Print the log line from yt-dlp

    # Wait for the process to finish
    process.wait()

    # Check if the downloaded file exists
    downloaded_files = [f for f in os.listdir("D:\Physicswallah") if os.path.isfile(os.path.join("D:\Physicswallah", f)) and f.endswith(".mp4")]
    if downloaded_files:
        print("Download completed!")
    else:
        print("Download failed!")

if __name__ == '__main__':
    app.run(debug=True)
