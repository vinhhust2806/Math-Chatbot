
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from langchain.document_loaders import UnstructuredFileLoader
import os
device = "cuda:0"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16)

model_id = "microsoft/Phi-3-mini-4k-instruct"  
tokenizer = AutoTokenizer.from_pretrained('local_model')        # Load Tokenizer

model = AutoModelForCausalLM.from_pretrained(              # Load Model
    'local_model1', 
    quantization_config=bnb_config,
    device_map="cuda", 
    torch_dtype="auto", 
    trust_remote_code=True, 
)

def generate_prompt(question):
  return f"""<|user|>\n"Answer the question following this format: Step 1: Step 2: Step 3: The final:. The question is: "+{question} <|end|>\n<|assistant|>
    """
def generate_python(question):
  return f"""<|user|>\n""Give the python code to solve this question:""+{question} <|end|>\n<|assistant|>
    """

def generate_pdf(question):
  return f"""<|user|>\n{question}<|end|>\n<|assistant|>
    """

def response(question):
    text = generate_prompt(question)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=500)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
def response_python(question):
    text = generate_python(question)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=500)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def response_pdf(question):
    text = generate_pdf(question)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=500)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def process_uploaded_files(uploaded_files):
    documents = []
    metadata = []
    for uploaded_file in uploaded_files:

        file_path = os.path.join(os.getcwd(), uploaded_file.name)

        # Save the uploaded file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        loader = UnstructuredFileLoader(file_path)
        loaded_documents = loader.load()
        documents.append(loaded_documents[0].page_content)
        metadata.append({"title":loaded_documents[0].metadata['source']})
    return documents, metadata