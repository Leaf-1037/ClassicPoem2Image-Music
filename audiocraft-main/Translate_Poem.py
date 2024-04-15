from transformers import AutoModelWithLMHead,AutoTokenizer,pipeline

mode_name = 'liam168/trans-opus-mt-zh-en'

model = AutoModelWithLMHead.from_pretrained(mode_name)
tokenizer = AutoTokenizer.from_pretrained(mode_name)
translation = pipeline("translation_zh_to_en", model=model, tokenizer=tokenizer)

def poem_translate(description: str):
    translation_result = translation(description, max_length=400)
    translation_text = translation_result[0]['translation_text']
    return translation_text

#print(poem_translate('我喜欢学习数据科学和机器学习。'))