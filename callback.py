import pyaudio
import wave

class AudioFile:
    chunk = 1024

    def __init__(self, filepath):
        """ Init audio stream """
        self.wf = wave.open(filepath, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Graceful shutdown """
        self.stream.close()
        self.p.terminate()

# Usage example for pyaudio
# a = AudioFile(r"C:\Users\dieul\research18\py2\audio\yakisobamono.wav")
# a.play()
# a.close()