from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Use model directly without downloading
g1_model = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer") 
g2_model = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-race-Distractor")
g1_tokenizer = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")
g2_tokenizer = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-race-Distractor")

# save models
g1_model.save_pretrained("./models/g1_model")
g2_model.save_pretrained("./models/g2_model")

# save tokenizer
g1_tokenizer.save_pretrained("./models/g1_tokenizer")
g2_tokenizer.save_pretrained("./models/g2_tokenizer")