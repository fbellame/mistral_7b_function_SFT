from transformers import AutoModelForCausalLM, AutoTokenizer
import time


device = "cuda" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained("fbellame/mistral-7b-json-quizz-fine-tuned")
tokenizer = AutoTokenizer.from_pretrained("fbellame/mistral-7b-json-quizz-fine-tuned")

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
Question: Qui va présenter le sujet des Comets à Extia?

A: Farid
B: Maxime
C: Jean
D: Farid et Maxime
Answer: D
[/INST]
"""

##################

encodeds = tokenizer(text_1, return_tensors="pt", add_special_tokens=False)

model_inputs = encodeds.to(device)
model.to(device)

st_time = time.time()
generated_ids = model.generate(**model_inputs, max_new_tokens=200, do_sample=False)
print(time.time()-st_time)

decoded = tokenizer.batch_decode(generated_ids)
print(decoded[0])

#################
