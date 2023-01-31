from transformers import AutoModel, AutoTokenizer
import os

print("Downloading model...")
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
model = AutoModel.from_pretrained(pretrained_model_name_or_path="VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
print("Saving model to disk...")
current_folder = os.path.dirname(os.path.realpath(__file__))
model_folder = os.path.join(current_folder, "model")
tokenizer.save_pretrained(model_folder)
model.save_pretrained(model_folder)
print("Finished caching model!")
