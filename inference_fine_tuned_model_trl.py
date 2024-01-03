from transformers import AutoModelForCausalLM, AutoTokenizer
import time


def print_model_response(decoded):
    
  output = decoded[0]

  # Find the first occurrence of '<</SYS>>'
  first_eos_position = output.find('<</SYS>>')

  # If the first occurrence is found, find the second occurrence
  if first_eos_position != -1:
      # Start the next search right after the first '<</SYS>>'
      second_eos_position = output.find('<</SYS>>', first_eos_position + len('<</SYS>>'))

      # If the second occurrence is found, truncate the output
      if second_eos_position != -1:
          output = output[:second_eos_position + len('<</SYS>>')]

  print(output)


device = "cuda" # the device to load the model onto
#fbellame/mistral-7b-json-quizz-fine-tuned
model = AutoModelForCausalLM.from_pretrained("fbellame/mistral-7b-json-quizz-fine-tuned-trl")
tokenizer = AutoTokenizer.from_pretrained("fbellame/mistral-7b-json-quizz-fine-tuned-trl")

#tokenizer.pad_token_id = 0
tokenizer.add_tokens('<</SYS>>')

eos_token_id = tokenizer.convert_tokens_to_ids('<</SYS>>')

#
# complete question, 
# Answer is not bad but get JSON markdown format like in a chat window, we don't wnat that
text_1 = """[INST]<<SYS>>
{
  "params": {
    "questions": [
      {
        "question": "question 1",
        "A": "choice A",
        "B": "choice B",
        "C": "choice C",
        "D": "choice D",
        "reponse": "right answer A or B or C or D"
      }
    ]
  }
}
<</SYS>>
Use the json definition above to generate a json with this quizz:
Question: Which programming language is known for its use in web development, particularly for its role in building the dynamic aspects of websites?

A: C++
B: Python
C: JavaScript
D: Java
Answer: C
[/INST]
"""


#
# Incomplete question, The model don't response with only json, add text
# No JSON stability
text_2 = """[INST]<<SYS>>
{
  "params": {
    "questions": [
      {
        "question": "question 1",
        "A": "choice A",
        "B": "choice B",
        "C": "choice C",
        "D": "choice D",
        "reponse": "right answer A or B or C or D"
      }
    ]
  }
}
<</SYS>>
Use the json definition above to generate a json with this quizz:
Blue
[/INST]
"""

##################

encodeds = tokenizer(text_1, return_tensors="pt", add_special_tokens=True)

model_inputs = encodeds.to(device)
model.to(device)

st_time = time.time()
generated_ids = model.generate(**model_inputs, max_new_tokens=200, do_sample=False, eos_token_id = eos_token_id)
print(time.time()-st_time)

decoded = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

print_model_response(decoded)

#################

encodeds = tokenizer(text_2, return_tensors="pt", add_special_tokens=True)

model_inputs = encodeds.to(device)
model.to(device)

st_time = time.time()
generated_ids = model.generate(**model_inputs, max_new_tokens=200, do_sample=False, eos_token_id = eos_token_id)
print(time.time()-st_time)
decoded = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

print_model_response(decoded)

#################
