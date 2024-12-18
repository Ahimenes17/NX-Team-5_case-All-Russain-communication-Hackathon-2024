from argparse import ArgumentParser
from speechkit import model_repository, configure_credentials, creds
from speechkit.stt import AudioProcessingType
from config import *


text = 'Здравствуйте. Вас приветствует общество с ограниченной ответственностью \"Лукоморье\". Мы можем предоставить вам Кота-Учёного, рассказывающего последние новости три девятого царства, Русалку, которая на ветвях сидит и постоянно соскальзывает, и остальных сказочных персонажей. Также в нашем ассортименте имеются: настойка из мухоморов, каша из топора, живая и мёртвая вода, трын-трава, сапоги-скороходы, скатерть-самобранка и другие интересные предметы быта. Вы также можете вызвать **на** дом Бабу Игу и Кощ+ея Бессм+ертного. Данный разговор записывается. ваш звонок очень важен для нас. Мы вас слушаем!'
text2 = 'Вы позвонили в туристическое агенство \"Р+уссо Тур+исcто\". Мы предоставляем туристические поездки на остров Буян, Хутор близ Диканьки, Калинов мост и Лысую гору. Данный разговор записывается. ваш звонок очень важен для нас. Мы вас слушаем!'
text3 = '- Ты же программист? В электрике шаришь, получается... Надо траншею под кабель прокопать метров 500.'

folderId ="b1gbe99p9gigsng6gcd0"

# Аутентификация через API-ключ.
configure_credentials(
   yandex_credentials=creds.YandexCredentials(
        iam_token='t1.9euelZqYm42JzZGdkJSJmsjHm4yPlu3rnpWanp6Sl5vNmIuTkZSdks-Wys_l8_d4WBVG-e8VfEoc_t3z9zgHE0b57xV8Shz-zef1656Vms2JzIqUysiSzYuNyMfJyJWZ7_zF656Vms2JzIqUysiSzYuNyMfJyJWZ.Hw2xgS0A0Jfsl1BNXII6smeFPT2tC7uzO3yAPiwcEquSYwRQx7r9Ik5NqnAITLoddxAsxwhBGPiRJbrJWINtDw'
   )
)


def recognize(audio):
   model = model_repository.recognition_model()

   # Задайте настройки распознавания.
   model.model = 'general'
   model.language = 'ru-RU'

   model.audio_processing_type = AudioProcessingType.Full

   # Распознавание речи в указанном аудиофайле и вывод результатов в консоль.
   result = model.transcribe_file(audio)
   for c, res in enumerate(result):
      print('=' * 80)
      print(f'channel: {c}\n\nraw_text:\n{res.raw_text}\n\nnorm_text:\n{res.normalized_text}\n')
      if res.has_utterances():
         print('utterances:')
         for utterance in res.utterances:
            print(utterance)

def synthesize(text, export_path):
   model = model_repository.synthesis_model(custom_headers=[("x-folder-id", folderId)])

   # Задайте настройки синтеза.
   model.voice = 'marina'
   model.role = 'friendly'
   model.speed = 0.8

   # Синтез речи и создание аудио с результатом.
   result = model.synthesize(text, raw_format=False)
   result.export(export_path, 'wav')


if __name__ == '__main__':
   parser = ArgumentParser()
   
   args = parser.parse_args()

   synthesize(text, '/var/lib/asterisk/sounds/welcome.wav')
   synthesize(text2, '/var/lib/asterisk/sounds/welcome1.wav')
   synthesize(text3, '/var/lib/asterisk/sounds/welcome2.wav')