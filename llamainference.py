import numpy as np
import copy
import torch
from transformers import AutoModelForCausalLM, LlamaTokenizer

test_token_num = 923
hf_model_location = ""
tokenizer = LlamaTokenizer.from_pretrained(hf_model_location,
                                            legacy=False,
                                            padding_side='left')
model = AutoModelForCausalLM.from_pretrained(hf_model_location)

model.half()
model.cuda()

def summarize_hf(text, temperature=1, output_len = 100, top_k=1, num_beams=1):
    line_encoded = tokenizer(text,
                                return_tensors='pt',
                                padding=True,
                                truncation=True)["input_ids"].type(torch.int64)

    line_encoded = line_encoded[:, -test_token_num:]
    line_encoded = line_encoded.cuda()

    with torch.no_grad():
        output = model.generate(line_encoded,
                                max_length=len(line_encoded[0]) +
                                output_len,
                                top_k=top_k,
                                temperature=temperature,
                                eos_token_id=tokenizer.eos_token_id,
                                pad_token_id=tokenizer.pad_token_id,
                                num_beams=num_beams,
                                num_return_sequences=num_beams,
                                early_stopping=True)

    tokens_list = output[:, len(line_encoded[0]):].tolist()
    output = output.reshape([1, num_beams, -1])
    output_lines_list = [
        tokenizer.batch_decode(output[:, i, len(line_encoded[0]):],
                                skip_special_tokens=True)
        for i in range(num_beams)
    ]

    return output_lines_list, tokens_list

if __name__ == "__main__":
    output, tokens = summarize_hf("TensorRT-LLM provides users with an easy-to-use Python API to define Large Language Models (LLMs) and build TensorRT engines that contain state-of-the-art optimizations to perform inference efficiently on NVIDIA GPUs. TensorRT-LLM also contains components to create Python and C++ runtimes that execute those TensorRT engines.")
    print(output)
    print(tokens)