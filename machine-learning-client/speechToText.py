"""use Google Cloud Speech-To-Text API"""
import io
from google.cloud import speech
from pydub import AudioSegment


def convert_stereo_to_mono(input_wav, output_wav):
    """convert a double channel wav to a single channel wav"""
    audio = AudioSegment.from_wav(input_wav)

    audio = audio.set_channels(1)

    audio.export(output_wav, format="wav")


def run_quickstart(local_file_path) -> speech.RecognizeResponse:
    """get transcript from google cloud speech-to-text"""
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    # gcs_uri = "machine-learning-client/77837^goodmrng.mp3"
    # gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"
    # audio = speech.RecognitionAudio(uri=gcs_uri)
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    # print(content)
    audio = {"content": content}

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    print(response)
    output = ""
    for result in response.results:
        output += f"{result.alternatives[0].transcript}"
    return output


def get_transcript():
    """main function"""
    input_wav = "uploads/audio.wav"
    output_wav = "curr.wav"
    #turns current audio to single channel and then transcribe
    convert_stereo_to_mono(input_wav, output_wav)
    return run_quickstart(output_wav)
