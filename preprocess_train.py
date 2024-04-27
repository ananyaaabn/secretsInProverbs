import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
from sklearn.model_selection import train_test_split

# Loading the dataset
df = pd.read_excel('datasets/proverbs.xlsx', usecols=['Id', 'Proverb', 'Translation', 'Genre', 'Meaning', 'Usage', 'language'], engine='openpyxl')

# Split the dataset dataset
train_df, val_df = train_test_split(df, test_size=0.2)

# Loading tokenizer and model
model_checkpoint = "Helsinki-NLP/opus-mt-ur-en"  
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)



# Tokenize datasets
train_dataset = Dataset.from_pandas(train_df)
train_dataset = train_dataset.map(lambda examples: tokenizer(examples["Proverb"], 
                                                            padding=True, 
                                                            truncation=True, 
                                                            return_tensors="pt"), 
                                 batched=True)

val_dataset = Dataset.from_pandas(val_df)
val_dataset = val_dataset.map(lambda examples: tokenizer(examples["Proverb"], 
                                                        padding=True, 
                                                        truncation=True, 
                                                        return_tensors="pt"), 
                             batched=True)
