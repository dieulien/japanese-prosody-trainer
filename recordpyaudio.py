"""
PyAudio example: Record a few seconds of audio and save to a WAVE
file.
"""

import pyaudio
import wave


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "speakers.wav"


def record_via_pyaudio(outputfn, start_function, done_function):

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    start_function()
    # print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    done_function()
    # print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outputfn, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def start_do():
    print("*recording")


def done_do():
    print("*done recording")


# record_via_pyaudio(r"C:\Users\dieul\research18\py2\audio\speakers.wav",start_do,done_do)

# open(rate,
#      format,
#      channels,
#      input=False,
#      output=False,
#      input_device_index=None,
#      output_device_index=None,
#      frames_per_buffer=1024,
#      start=True,
#      input_host_api_specific_stream_info=None,
#      output_host_api_specific_stream_info=None,
#      stream_callback=None)

# def callback(in_data, frame_count,
#              time_info, status_flags):
#     # PROCESSING
#     out_data = in_data
#     return (out_data, pyaudio.PaContinue)