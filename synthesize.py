from argparse import ArgumentParser
from speechkit import model_repository, configure_credentials, creds
from speechkit.stt import AudioProcessingType
from config import *


text = 'Здравствуйте, Вас приветствует ООО \"Лукоморье\". Мы можем предоставить вам Кота-Учёного, рассказывающего сказки и поющего песни, Русалку, которая на ветвях сидит и постоянно соскальзывает, тридцать три богатыря, Дядьку Черномора и остальных сказочных персонажей. Также в нашем ассортименте имеются: настойка из мухоморов, каша из топора, живая и мёртвая вода, трын-трава, сапоги-скороходы, скатерть-самобранка и другие интересные предметы быта. Вы также можете вызвать н+а **дом** Б+абу Яг+у и Кощея Бессмертного. Данный разговор записывается. Мы вас слушаем!'
folderId ="b1gbe99p9gigsng6gcd0"

# Аутентификация через API-ключ.
configure_credentials(
   yandex_credentials=creds.YandexCredentials(
        iam_token='t1.9euelZrIz8-dm5iKx8aYm56PlZ7MzO3rnpWanp6Sl5vNmIuTkZSdks-Wys_l8_cXbxlG-e9beB5L_N3z91cdF0b571t4Hkv8zef1656Vmo7Jl4vLlouQl5vHm5TPzJqO7_zF656Vmo7Jl4vLlouQl5vHm5TPzJqO.sylfBISMcJP55out8MhDh1zTWCedCc5T7cGbf5bTsILNoEJH2pP57TKKM4Z3ocP9OT6TianiAptBR6URMmapAA'
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
   model.voice = 'jane'
   model.role = 'good'

   # Синтез речи и создание аудио с результатом.
   result = model.synthesize(text, raw_format=False)
   result.export(export_path, 'wav')


if __name__ == '__main__':
   parser = ArgumentParser()
   
   args = parser.parse_args()

   synthesize(text, 'welcome.wav')