
import os
from langchain.document_loaders import UnstructuredFileLoader
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline

device = "cuda:0"

model_id = "microsoft/Phi-3-mini-4k-instruct"  

tokenizer = AutoTokenizer.from_pretrained('microsoft/Phi-3-mini-4k-instruct')        

model = AutoModelForCausalLM.from_pretrained(           
    'microsoft/Phi-3-mini-4k-instruct', 
    device_map="cuda", 
    torch_dtype="auto", 
    trust_remote_code=True, 
)

pipe = pipeline( 
    "text-generation", 
    model=model, 
    tokenizer=tokenizer, 
) 

generation_args = { 
    "max_new_tokens": 500, 
    "return_full_text": False, 
    "temperature": 0.0, 
    "do_sample": False, 
} 

def answer(text):
   messages = [ 
    {"role": "system", "content": "You are a helpful AI assistant."}, 
    {"role": "user", "content": text}
              ] 
   output = pipe(messages, **generation_args) 
   return output[0]['generated_text']

def answer_context(text, context):
   messages = [ 
    {"role": "system", "content": "You are a helpful AI assistant."}, 
    {"role": "user", "content": f"The context is {context}. Give the answer relating to context if the following requirement relating to context, if not, give normal answer. The requirement is: " + text}
              ] 
   output = pipe(messages, **generation_args) 
   return output[0]['generated_text']

def answer_python(text):
   messages = [ 
    {"role": "system", "content": "You are a helpful AI assistant."}, 
    {"role": "user", "content": "Give the python code to solve this question: " + text}
              ] 
   output = pipe(messages, **generation_args) 
   return output[0]['generated_text']

def answer_step(text):
   messages = [ 
    {"role": "system", "content": "You are a helpful AI assistant."}, 
    {"role": "user", "content": "Answer the question following this format: Step 1: Step 2: Step 3: The final:. The question is: " + text}
              ] 
   output = pipe(messages, **generation_args) 
   return output[0]['generated_text']

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