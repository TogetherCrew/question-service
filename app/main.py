from transformers import pipeline
from pydantic import BaseModel
from fastapi import FastAPI


app = FastAPI()
model = "shahrukhx01/question-vs-statement-classifier"
pipe = pipeline("text-classification", model=model)


custom_labels = {"LABEL_0": "STATEMENT", "LABEL_1": "QUESTION"}


class Payload(BaseModel):
    text: str


@app.post("/test")
async def test(payload: Payload):
    result = pipe(payload.text)[0]

    # Customize the label
    result["label"] = custom_labels.get(result["label"], result["label"])
    return result
