from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
import torch
import torchaudio
from audiocraft.data.audio import audio_write

# 第一个参数是指用哪一个模型 详见官方github
model = musicgen.MusicGen.get_pretrained('melody', device='cuda')

def generate_music(description_cn: str,description: str,filedir: str,duration=30,user_upload=False):
    # 这里调整描述词
    # discriptions = [
    #     'crazy EDM, heavy bang', 
    #     'classic reggae track with an electronic guitar solo',
    #     'lofi slow bpm electro chill with organic samples',
    #     'rock with saturated guitars, a heavy bass line and crazy drum break and fills.',
    #     'earthy tones, environmentally conscious, ukulele-infused, harmonic, breezy, easygoing, organic instrumentation, gentle grooves',
    # ]

    # 这里调整生成时长
    model.set_generation_params(duration=duration)
    print(f'BASERHYTHM: {filedir}')
    melody, sr = torchaudio.load(filedir)
    #melody, sr = torchaudio.load('./assets/bach.mp3')
    # 测试用 只用最后一个提示词
    #res = model.generate(discription , progress=True)
    # 控制description长度
    description = description[:40]
    print(f'DESCRIPTION: {description}')
    descriptions = description.split(",")
    dlength = len(descriptions)
    wav = model.generate_with_chroma(descriptions, melody[None].expand(dlength, -1, -1), sr)
    #display_audio(res, 32000)
    for idx, one_wav in enumerate(wav):
        if idx > 0:
            break
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        audio_write(f'MusicRes/{description_cn}', one_wav.cpu(), model.sample_rate, strategy="loudness")
    return "/root/autodl-fs/audiocraft-main/MusicRes/"+description_cn+".wav"

#generate_music('大弦嘈嘈如急雨','')