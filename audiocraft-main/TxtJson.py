import json  

# 假设你的txt文件名为'input.txt'    
def Transform_Form():  
    with open('/root/autodl-fs/Fengshenbang-LM/PromptRes/Statistics.txt', 'r', encoding='utf-8') as in_file:    
        # 读取并解析txt文件的内容    
        pairs = [line.strip().split()[::-1] for line in in_file.readlines()]  
        print(f'pairs={pairs}')
        dictionary = {item[1]: int(item[0]) for item in pairs}    
      
    # 将字典转为json格式并保存到json文件中，假设json文件名为'output.json'    
    with open('/root/autodl-fs/Fengshenbang-LM/PromptRes/Statistics.json', 'w', encoding='utf-8') as out_file:    
        #json.dump(dictionary, out_file) 
        out_file.write(json.dumps(dictionary, ensure_ascii=False)) 
  
#Transform_Form()