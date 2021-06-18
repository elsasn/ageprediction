from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

import streamlit as st

st.title('Upload Image File ti Streamlit')
uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

camera = cv2.VideoCapture(0)  # use 0 for web camera
input = st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = input.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = input.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)