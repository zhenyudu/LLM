from langchain_community.chat_models import ChatOllama

class ModelLoader:

    @classmethod
    def ollama_loader(cls, model_name: str = "llama3.2", **params):
        model = ChatOllama(model=model_name, **params)
        return model
    
    @classmethod
    def llamacpp_loader(cls, model_name: str, **params):
        # from langchain_community import LlamaCpp
        # from transformers import AutoTokenizer

        # tokenizer_path = # TODO: get tokenizer path
        # model_path = # TODO: get model path
        # tokenizer = Autotokenizer.from_pretrained(tokenizer_path)
        # model = LlamaCpp(
        #     model_path    = model_path,
        #     device        = "mps",
        #     n_gpu_layers  = -1,
        #     n_batch       = 512,
        #     n_ctx         = 2048,
        #     *params)
        pass

    @classmethod
    def transformer_loader(cls, model_name: str, **params):
        # from transformers import AutoTokenizer, AutoModelCausalLM
        # import torch

        # tokenizer_path = # TODO: get tokenizer path
        # model_path = # TODO: get model path
        # tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        # llm = AutoModelCausalLM.from_pretrained(
        #     model_path,
        #     device_map="auto",
        #     torch_dtype=torch.float16,
        #     load_in_8bit=True,
        #     **params)
        pass


# class LlamaCppInvokeBody:

#     def __init__(self, tokenizer, model) -> None:
#         self.tokeizer   = tokenizer
#         self.model      = model

#     def invoke(self, message, **params):
#         prompt = self.tokeizer.apply_chat_tempalte(message, tokenize=False, add_generation_prompt=True)
#         return self.model(prompt, **params)
    

# class TransformersInvokeBody:

#     def __init__(self, tokenizer, model) -> None:
#         self.tokeizer   = tokenizer
#         self.model      = model

#     def invoke(self, message, **params):
#         params['max_new_tokens']        = params['max_tokens']
#         params['repetition_penalty']    = params['repeat_penalty']
#         del params['max_tokens'], params['repeat_penalty']

#         input_ids = self.tokeizer.apply_chat_tempalte(message, return_tensors="pt", add_generation_prompt=True).to(self.model.device)
#         outputs = self.model.generate(input_ids, **params, eos_token_id=[self.tokeizer.eos_token_id, self.tokeizer.convert_tokens_to_ids("<eot_id>")])
#         response = outputs[0][input_ids.shape[-1]:]
#         return self.tokeizer.decode(response, skip_special_tokens=True)