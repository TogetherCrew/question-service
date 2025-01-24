import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    q = asyncio.Queue()
    app.model_queue = q
    task = asyncio.create_task(server_loop(q))
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)
model = "shahrukhx01/question-vs-statement-classifier"


custom_labels = {"LABEL_0": "STATEMENT", "LABEL_1": "QUESTION"}


class Payload(BaseModel):
    text: str


@app.post("/test")
async def test(payload: Payload, request: Request):
    print(payload)
    response_q = asyncio.Queue()
    await request.app.model_queue.put((payload.text, response_q))
    output = await response_q.get()
    print(output)
    result = output[0]

    # Customize the label
    result["label"] = custom_labels.get(result["label"], result["label"])
    print(result)
    return result


async def server_loop(q):
    pipe = pipeline("text-classification", model=model)
    while True:
        (string, response_q) = await q.get()
        out = pipe(string)
        await response_q.put(out)
