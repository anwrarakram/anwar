# a2f_client.py
import grpc
import a2f_pb2
import a2f_pb2_grpc

def send_audio_to_a2f(wav_path: str, host: str = 'localhost:50051'):
    """将 WAV 音频发送给 Audio2Face 的 gRPC 服务，触发嘴型播放"""
    
    # 连接 gRPC 服务
    channel = grpc.insecure_channel(host)
    stub = a2f_pb2_grpc.AudioToFaceStub(channel)

    # 读取音频数据
    with open(wav_path, 'rb') as f:
        audio_bytes = f.read()

    # 构造请求
    request = a2f_pb2.SubmitAudioRequest(
        audio_data=audio_bytes,
        sample_rate=16000,    # 百度 TTS 默认 16000Hz
        stream_mode=False     # 非流式模式：一次性发送全部音频
    )

    # 发送请求并获取响应
    response = stub.SubmitAudio(request)
    print("Audio2Face 回复：", response.status)
