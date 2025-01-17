from flask import Flask, render_template, request, Response, redirect, url_for, jsonify
import os
import logging

from backend import (
    start_processing_thread,
    get_crash_count,
    get_log_file_path,
    mark_crash_now,
    is_video_done,
    get_extraction_progress,
    toggle_pause,
    skip_video
)

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link', '')
        folder_name = request.form.get('folder_name', '')
        delete_original = True if request.form.get('delete_original') == 'on' else False

        start_processing_thread(
            youtube_link=youtube_link,
            folder_name=folder_name,
            delete_original=delete_original
        )

        return redirect(url_for('view_stream'))

    return render_template('index.html')

@app.route('/view_stream')
def view_stream():
    return render_template('results.html')

@app.route('/video_feed')
def video_feed():
    from backend import generate_video_stream
    return Response(
        generate_video_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/mark_crash', methods=['POST'])
def mark_crash():
    mark_crash_now()
    return ('', 204)

@app.route('/check_status')
def check_status():
    if is_video_done():
        return "done"
    else:
        return "running"

@app.route('/get_crash_count')
def get_crash_count_api():
    count = get_crash_count()
    return str(count)

@app.route('/get_extraction_progress')
def get_extraction_progress_api():
    progress = get_extraction_progress()
    return progress

@app.route('/final_results')
def final_results():
    crash_count = get_crash_count()
    log_file_path = get_log_file_path()
    return render_template(
        'final.html',
        crash_count=crash_count,
        log_file_path=log_file_path
    )

@app.route('/toggle_pause', methods=['POST'])
def pause_resume():
    paused = toggle_pause()
    return jsonify({"paused": paused}), 200

@app.route('/rewind', methods=['POST'])
def rewind_video():
    skip_video(-10)
    return ('', 204)

@app.route('/fast_forward', methods=['POST'])
def fast_forward_video():
    skip_video(10)
    return ('', 204)

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.logger.disabled = True

    app.run(host='0.0.0.0', port=5000, debug=False)
