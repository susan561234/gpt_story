import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from pydub import AudioSegment#轉mp3
import configparser
import os


config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config.read(os.path.join(BASE_DIR ,'config.ini'))
config.get('voice', 'speech_key')
def STT(text="說出一句話"):
    #先config
    speech_config = speechsdk.SpeechConfig(subscription=config.get('voice', 'speech_key'), region=config.get('voice', 'service_region'), speech_recognition_language='zh-tw')
    #創建分辨器
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config = speech_config)
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

def TTS(text):
    speech_config = speechsdk.SpeechConfig(subscription=config.get('voice', 'speech_key'), region=config.get('voice', 'service_region'))

    # The full list of supported languages can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support#text-to-speech
    #設定語系或是設定指定人的聲音(擇一)
    
    # #特定語系
    language = "zh-TW"
    speech_config.speech_synthesis_language = language

    # #特定人聲
    voice = "zh-CN-XiaoyiNeural"
    voice2 = "zh-CN-XiaoshuangNeural"
    speech_config.speech_synthesis_voice_name = voice
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    
    result = speech_synthesizer.speak_text_async(text).get()
    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file("./static/Resources/Hiyori/sounds/filelive2d"+".wav")
  
# def TTS(text,option_count):
#     speech_config = speechsdk.SpeechConfig(subscription=config.get('voice', 'speech_key'), region=config.get('voice', 'service_region'))

#     #設定語系或是設定指定人的聲音(擇一)
#     # #特定語系
#     language = "zh-TW"
#     speech_config.speech_synthesis_language = language

#     # #特定人聲
#     voices = ["zh-CN-XiaoyiNeural", "zh-CN-XiaoshuangNeural"]
#     speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)

#     for i, voice in enumerate(voices):
#         if i ==0:
#             speech_config.speech_synthesis_voice_name = voice
#             speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
#             result = speech_synthesizer.speak_text_async(text).get()
#             stream = speechsdk.AudioDataStream(result)
#             stream.save_to_wav_file(f"./static/file{option_count}.wav")
#             wav_file = AudioSegment.from_wav(f"./static/file{option_count}.wav")
#             wav_file.export(f"./static/file{option_count}.mp3", format="mp3") 
#         if i ==1:
#             speech_config.speech_synthesis_voice_name = voice
#             speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
#             result = speech_synthesizer.speak_text_async(text).get()
#             stream = speechsdk.AudioDataStream(result)
#             stream.save_to_wav_file("./static/Resources/Hiyori/sounds/filelive2d"+".wav")


# if __name__ =="__main__":
#     print("測試打一句話")
#     text = input()
#     TTS(text)