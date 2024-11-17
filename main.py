from config import *
import os
import argparse
from asterisk.agi import *
import requests
import grpc
import yandex.cloud.ai.stt.v2.stt_service_pb2 as stt_service_pb2
import yandex.cloud.ai.stt.v2.stt_service_pb2_grpc as stt_service_pb2_grpc

agi = AGI()
CHUNK_SIZE = 4000
folder = folder_id
iam_token = token
dataForSpeech = data

