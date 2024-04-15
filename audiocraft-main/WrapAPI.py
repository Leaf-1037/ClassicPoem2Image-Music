import tornado.ioloop
import tornado.web
import tornado.options
import os
import re
from tornado.options import options, define, parse_command_line

import platform

from ImageGen import generate_image

#sys.path.append('/root/autodl-fs/audiocraft-main/')

from MusicGen import generate_music

from calculate_words import Get_Statistics

from Translate_Poem import poem_translate

def Get_BaseMusic(text2music:str):
    Resfile=""
    if "悠扬" in text2music:
      if "抒情" in text2music:
        Resfile="为霜.mp3"
      else:
        Resfile="寻一个你.mp3"
    elif "抒情" in text2music:
      if "神秘" in text2music:
        Resfile="五月雨.mp3"
      elif "宏大" in text2music:
        Resfile="Camping.mp3"
      elif "哲理" in text2music:
        Resfile="Arrival of the Birds.mp3"
      elif "神秘" in text2music:
        Resfile="月亮之子.mp3"
      elif "欢快" in text2music:
        Resfile="清韵.mp3"
      elif "繁华" in text2music:
        Resfile="水龙吟.mp3"
      else:
        Resfile="痴情冢.mp3" 
    elif "神秘" in text2music:
      Resfile="reset.mp3"
    elif "欢快" in text2music:
      Resfile="圣诞节的雪.mp3"
    elif "徘徊" in text2music:
      Resfile="忍受.mp3"
    elif "哲理" in text2music:
      if "宏大" in text2music:
        Resfile="Experience.mp3"
      else:
        Resfile="In The Background.mp3"
    elif "宏大" in text2music:
      Resfile="Cornfield Chase.mp3"
    elif "繁华" in text2music:
      Resfile="双面燕洵.mp3"
    else:
      Resfile="Bloom of Youth.mp3"
    return "/root/autodl-fs/audiocraft-main/assets/"+Resfile

def Get_Next_Filename():
  # 获取文件夹中所有.txt文件的文件名  
    txt_files = [f for f in os.listdir('/root/autodl-fs/finetune_taiyi_stable_diffusion/demo_dataset/part_0/') if f.endswith('.txt')]  
    # 如果没有.txt文件，返回None  
    if not txt_files:  
        return ""
    # 获取最大的文件名  
    largest_filename = max(txt_files, key=lambda x: x)  
    print(f'largest_filename={largest_filename}')
    largest_order = int(largest_filename[:-4])
    next_filename=str(largest_order + 1)
    while len(next_filename) < 8:
      next_filename = '0' + next_filename
    return next_filename

def pre_process(process_str:str):
  process_str = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+","", process_str) 
  exception_str=["悠扬","抒情","神秘","欢快","徘徊","哲理","宏大","繁华"]
  for estr in exception_str:
    process_str = process_str.replace(estr,'')
  return process_str

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    print("GET Request!")

    # 允许跨域访问
    self.set_header("Access-Control-Allow-Origin","*")

    # 获取参数，如果没有置为空
    negative_prompt = ''
    guidance_scale = ''
    num_inference_steps = ''
    seed = ''
    height = ''
    width = ''

    negative_prompt = self.get_query_argument('negative_prompt','')
    guidance_scale = self.get_query_argument('guidance_scale','')
    num_inference_steps = self.get_query_argument('num_inference_steps','')
    seed = self.get_query_argument('seed','')
    height = self.get_query_argument('height','')
    width = self.get_query_argument('width','')
    print(f'negative_prompt={negative_prompt} guidance_scale={guidance_scale} num_inference_steps={num_inference_steps}')
    print(f'seed={seed} height={height} width={width}')

    text2image = self.get_query_argument('text2image', '')
    text2music = self.get_query_argument('text2music', '')
    renew = self.get_query_argument('renew', '')
    print(f'text2image={text2image} text2music={text2music} renew={renew}')

    # 根据解析参数设置资源地址
    if text2image!='':
      #resource_dir = "/root/autodl-fs/Fengshenbang-LM/ImageRes/"+text2image[:6]+".png"
      Next_Filename = Get_Next_Filename()
      with open('/root/autodl-fs/finetune_taiyi_stable_diffusion/demo_dataset/part_0/'+Next_Filename+'.txt', 'w') as file: 
        file.write(re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+"," ", text2image))
      with open('/root/autodl-fs/Fengshenbang-LM/PromptRes/PromptData.txt', 'a') as file: 
        file.write(text2image+'\n')
      Get_Statistics()
      resource_dir = generate_image(prompt=text2image,Next_Filename=Next_Filename,seed=seed,negative_prompt=negative_prompt,guidance_scale=guidance_scale,num_inference_steps=num_inference_steps,height=height,width=width)
    elif text2music!='':
      resource_dir = "/root/autodl-fs/audiocraft-main/MusicRes/"+text2music+".wav"
      #filedir=Get_BaseMusic(text2music)
      #generate_music(text2music,filedir,false)
    elif renew!='':
      resource_dir = "/root/autodl-fs/Fengshenbang-LM/PromptRes/Statistics.json"
    else:  
      return

    with open(resource_dir, 'rb') as resource_file:
        self.write(resource_file.read())
        # 设置响应头的内容类型为请求资源类型
        if text2image!='':
          self.set_header('Content-Type', 'image/png')
        elif text2music!='':
          #self.set_header('Content-Type', 'application/octet-stream')
          self.set_header('Content-Type','audio/wav')
        elif renew!='':
          self.set_header('Content-Type', 'application/json')
        self.finish()

class UploadHandler(tornado.web.RequestHandler): 
  def post(self):  
    print("POST Request!")

    # 允许跨域访问
    self.set_header("Access-Control-Allow-Origin","*")

    # 获取所有的请求参数  
    args = self.request.arguments  
    print("Arguments: ", args)  

    # 获取上传的文件  
    if 'file' in self.request.files:
      file = self.request.files['file']  

      # 获取文件名  
      filename = file[0]['filename']  
      print(f'\nPOST filename={filename}\n')
      # 确定保存文件的路径  
      save_path = "/root/autodl-fs/audiocraft-main/BasicRhythm/" + filename  
      # 将文件保存到指定路径  
      with open(save_path, 'wb') as f:  
        f.write(file[0]['body'])  
      # 返回响应  
      #self.write("File saved successfully")  

      if 'text2music' in args:
        text2music = args['text2music']
        print(f'PARAM: text2music={text2music}')
        text2music_pre=pre_process(text2music[0].decode('utf-8'))
        print(f'PARAM PROCESS: text2music={text2music_pre}')
        text2music_en = poem_translate(text2music_pre)
        #resource_dir = "/root/autodl-fs/audiocraft-main/MusicRes/"+text2music[0].decode('utf-8')+".wav"
        resource_dir = generate_music(text2music[0].decode('utf-8'),text2music_en,save_path,30,True)
        self.set_status(200)
      else:
        self.set_status(403)
        return
    else:
      print('\nNO POST FILE!\n')

      if 'text2music' in args:
        text2music = args['text2music']
        print(f'PARAM: text2music={text2music}')
        text2music_pre=pre_process(text2music[0].decode('utf-8'))
        print(f'PARAM PROCESS: text2music={text2music_pre}')
        text2music_en = poem_translate(text2music_pre)
        #resource_dir = "/root/autodl-fs/audiocraft-main/MusicRes/"+text2music[0].decode('utf-8')+".wav"
        #print(f'resource_dir={resource_dir}')
        filedir=Get_BaseMusic(text2music[0].decode('utf-8'))
        resource_dir = generate_music(text2music[0].decode('utf-8'),text2music_en,filedir,30,False)
        self.set_status(200) 
      else:
        self.set_status(403)  
        return

    with open(resource_dir, 'rb') as resource_file:
        self.write(resource_file.read())
        # 设置响应头的内容类型为请求资源类型
        self.set_header('Content-Type', 'application/octet-stream')
        #self.set_header('Content-Type','audio/wav')
        self.finish()

if __name__ == "__main__":
  port = 6006
  tornado.options.parse_command_line()
  app = tornado.web.Application([(r"/", MainHandler),(r"/upload",UploadHandler)])
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(port)
  tornado.ioloop.IOLoop.current().start()
  # print(Get_Next_Filename())