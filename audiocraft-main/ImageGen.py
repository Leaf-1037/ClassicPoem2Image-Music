import torch
from diffusers import StableDiffusionPipeline
import inspect  
import random
import re

pipe = StableDiffusionPipeline.from_pretrained("/root/autodl-fs/IDEA-CCNLTaiyi-Stable-Diffusion-1B-Chinese-v0.1",local_files_only=True).to("cuda")

def generate_image(prompt:str,Next_Filename:str,seed:str,negative_prompt:str,guidance_scale:str,num_inference_steps:str,height:str,width:str):
    # Prompt预处理：去除中文符号
    prompt = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+"," ", prompt) 
    if '油画' not in prompt:
        prompt = prompt + ' 油画'
    # 打印预处理后的Prompt
    print(f'\nprompt={prompt}\n')
    # 生成随机数种子
    if seed == '':
        seed_num = random.randint(1, 10000000000)
    else:
        seed_num = int(seed)
    # 调整negative_prompt
    if negative_prompt == '':
        negative_prompt = '广告, ，, ！, 。, ；, 资讯, 新闻, 水印'
    # 调整guidance_scale
    if guidance_scale == '':
        guidance_scale_num = 7.5
    else:
        guidance_scale_num = float(guidance_scale)
    # 调整num_inference_steps
    if num_inference_steps == '':
        num_inference_steps_num = 50
    else:
        num_inference_steps_num = int(num_inference_steps)
    # 调整height
    if height == '':
        height_num = 512
    else:
        height_num = int(height)
    # 调整width
    if width == '':
        width_num = 512
    else:
        width_num = int(width)
    # 生成器
    generator = torch.Generator("cuda").manual_seed(seed_num) 
    # 生成图像
    image = pipe(prompt=prompt, negative_prompt=negative_prompt, guidance_scale=guidance_scale_num, num_inference_steps=num_inference_steps_num, generator=generator,height=height_num, width=width_num).images[0]
    #image = pipe(prompt=prompt, generator=generator).images[0]
    
    # 探测pipe参数
    # sig = inspect.signature(pipe)  
    # for name, param in sig.parameters.items():  
    #     print(f'参数 {name} 是必需的') if param.default == inspect.Parameter.empty else print(f'参数 {name} 不是必需的')
    # 保存图片
    image.save("/root/autodl-fs/Fengshenbang-LM/ImageRes/"+prompt[:6]+".png")
    # 自学习机制——将生成的图像保存到数据集下
    image.save("/root/autodl-fs/finetune_taiyi_stable_diffusion/demo_dataset/part_0/"+Next_Filename+".jpg")
    return "/root/autodl-fs/Fengshenbang-LM/ImageRes/"+prompt[:6]+".png"

#generate_image('、、、飞流直下三千尺，……&&&&&&&&&&油画','','30','广告, ，, ！, 。, ；, 资讯, 新闻, 水印','7.5','40','512','512') 