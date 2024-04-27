from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Loading the trained model and tokenizer
model_path = "./trained_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Function to generate translation based on input text
def generate_translation(input_text):
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(model.device)
    # Using beam search and apply length penalty
    outputs = model.generate(input_ids, max_length=100, num_beams=4, length_penalty=0.6, early_stopping=True)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text
