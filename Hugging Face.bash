from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "distilgpt2"  # 小型GPTモデル
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

input_text = "Efa is a brilliant hacker who"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
output = model.generate(input_ids, max_length=50, do_sample=True)
print(tokenizer.decode(output[0], skip_special_tokens=True))
