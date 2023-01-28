from typing import List
from torch import no_grad, FloatTensor
from transformers import AutoModel, AutoTokenizer, PhobertTokenizer, RobertaModel
from transformers.modeling_outputs import BaseModelOutputWithPoolingAndCrossAttentions
from pyvi.ViTokenizer import tokenize
from transformers import logging


class Vectorize:
  MODEL_NAME = "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"

  def __init__(self, sentences: List[str]):
    self._input_sentences = sentences
    logging.set_verbosity_error()

  def handle(self):
    """
    https://huggingface.co/docs/transformers/v4.26.0/en/model_doc/roberta#transformers.RobertaModel
    PhoBert is based on RoBERTa
    """

    phobert_tokenizer: PhobertTokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=self.MODEL_NAME)
    sentences = [tokenize(sentence) for sentence in self._input_sentences]
    inputs = phobert_tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
    vectors = self._embed_inputs(inputs)
    return vectors

  def _embed_inputs(self, inputs):
    phobert_model: RobertaModel = AutoModel.from_pretrained(pretrained_model_name_or_path=self.MODEL_NAME)

    with no_grad():
      phobert_model_output: BaseModelOutputWithPoolingAndCrossAttentions = phobert_model(
        **inputs, output_hidden_states=True, return_dict=True
      )
      embeddings: FloatTensor = phobert_model_output.pooler_output
    return [vector.tolist() for vector in embeddings]
