import pyaudio


def list_insterfaces() -> dict:
    audio = pyaudio.PyAudio()
    audio_infos = {}
    audio_infos["num_host_audio"] = audio.get_host_api_count()
    audio_infos["devices"] = []
    for i_host in range(audio_infos["num_host_audio"]):
        infos = audio.get_host_api_info_by_index(i_host)
        for i_device in range(0, infos["deviceCount"]):
            device_infos = audio.get_device_info_by_host_api_device_index(
                i_host, i_device
            )
            max_input = device_infos["maxInputChannels"]
            if max_input > 0:
                audio_infos["devices"].append(
                    (device_infos["index"], device_infos["name"])
                )
    return audio_infos
