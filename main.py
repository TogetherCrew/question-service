from transformers import pipeline
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
pipe = pipeline("text-classification", model="shahrukhx01/question-vs-statement-classifier")

custom_labels = {
    "LABEL_0": "statement",
    "LABEL_1": "question"
}

class Payload(BaseModel):
  text: str

@app.post("/test")
async def test(payload: Payload):
  result = pipe(payload.text)[0]
  
  # Customize the label
  result['label'] = custom_labels.get(result['label'], result['label'])

  return result