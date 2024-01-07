import requests
import json

question = """[INST]<<SYS>>
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
[/INST]"""


url = "https://56y63gin7vewn2-80.proxy.runpod.net/generate"
headers = {'Content-Type': 'application/json'}

try:
    data = {"inputs":question,"parameters":{"max_new_tokens":200}}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()

    if response.status_code == 200:
        print(response_data["generated_text"])
    else:
        # Instead of printing here, you might raise an exception or return a special value.
        print(response.status_code)
except requests.exceptions.RequestException as e:
    # Instead of printing here, you might raise an exception or return a special value.
    print("Error: " + str(e))
