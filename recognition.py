import pyaudio
import wave
import argparse
import grpc
import yandex.cloud.ai.stt.v3.stt_pb2 as stt_pb2
import yandex.cloud.ai.stt.v3.stt_service_pb2_grpc as stt_service_pb2_grpc

# Настройки потокового распознавания.
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
CHUNK = 4096
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "audio.wav"

audio = pyaudio.PyAudio()

def gen():
   # Задайте настройки распознавания.
   recognize_options = stt_pb2.StreamingOptions(
      recognition_model=stt_pb2.RecognitionModelOptions(
         audio_format=stt_pb2.AudioFormatOptions(
            raw_audio=stt_pb2.RawAudio(
               audio_encoding=stt_pb2.RawAudio.LINEAR16_PCM,
               sample_rate_hertz=8000,
               audio_channel_count=1
            )
         ),
         text_normalization=stt_pb2.TextNormalizationOptions(
            text_normalization=stt_pb2.TextNormalizationOptions.TEXT_NORMALIZATION_ENABLED,
            profanity_filter=True,
            literature_text=False
         ),
         language_restriction=stt_pb2.LanguageRestrictionOptions(
            restriction_type=stt_pb2.LanguageRestrictionOptions.WHITELIST,
            language_code=['ru-RU']
         ),
         audio_processing_type=stt_pb2.RecognitionModelOptions.REAL_TIME
      )
   )

   # Отправьте сообщение с настройками распознавания.
   yield stt_pb2.StreamingRequest(session_options=recognize_options)

   # Начните запись голоса.
   stream = audio.open(format=FORMAT, channels=CHANNELS,
               rate=RATE, input=True,
               frames_per_buffer=CHUNK)
   print("recording")
   frames = []

   # Распознайте речь по порциям.
   for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read(CHUNK)
      yield stt_pb2.StreamingRequest(chunk=stt_pb2.AudioChunk(data=data))
      frames.append(data)
   print("finished")

   # Остановите запись.
   stream.stop_stream()
   stream.close()
   audio.terminate()

   # Создайте файл WAV с записанным голосом.
   waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
   waveFile.setnchannels(CHANNELS)
   waveFile.setsampwidth(audio.get_sample_size(FORMAT))
   waveFile.setframerate(RATE)
   waveFile.writeframes(b''.join(frames))
   waveFile.close()

def run(secret):
   # Установите соединение с сервером.
   cred = grpc.ssl_channel_credentials()
   channel = grpc.secure_channel('stt.api.cloud.yandex.net:443', cred)
   stub = stt_service_pb2_grpc.RecognizerStub(channel)

   # Отправьте данные для распознавания.
   it = stub.RecognizeStreaming(gen(), metadata=(
   # Параметры для аутентификации с API-ключом от имени сервисного аккаунта
   #   ('authorization', f'Api-Key {secret}'),
   # Для аутентификации с IAM-токеном используйте строку ниже
     ('authorization', f'Bearer {secret}'),
     ('x-folder-id', 'b1gbe99p9gigsng6gcd0')
   ))

   # Обработайте ответы сервера и выведите результат в консоль.
   try:
      for r in it:
         event_type, alternatives = r.WhichOneof('Event'), None
         if event_type == 'partial' and len(r.partial.alternatives) > 0:
            alternatives = [a.text for a in r.partial.alternatives]
         if event_type == 'final':
            alternatives = [a.text for a in r.final.alternatives]
         if event_type == 'final_refinement':
            alternatives = [a.text for a in r.final_refinement.normalized_text.alternatives]
         print(f'type={event_type}, alternatives={alternatives}')
   except grpc._channel._Rendezvous as err:
      print(f'Error code {err._state.code}, message: {err._state.details}')
      raise err

if __name__ == '__main__':
   secret = 't1.9euelZrOl8nMlMqekc6Pzs-RmsiZle3rnpWanp6Sl5vNmIuTkZSdks-Wys_l8_dCRRlG-e84Z0Y6_d3z9wJ0Fkb57zhnRjr9zef1656VmpmZx8iVj5KMkMjMlpKQjZSc7_zF656VmpmZx8iVj5KMkMjMlpKQjZSc.M7busXxTaKHzv4EigD2S93m_J1oYxgNYa7HAxd2m2n1Aez1EwkwlfrHQ4_I_HhWrI8ne5O106wO3CT5NzJp8AQ'
   #parser = argparse.ArgumentParser()
   #parser.add_argument('--secret', required=True, help='API key or IAM token')
   #args = parser.parse_args()
   run(secret)