from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from functools import partial
import time
from pydantic import BaseModel


###   Custom   ##########################################

import torch
from typing import List

# 模擬 GPU 任務
async def gpu_task(data: List[float]) -> float:
    # 將數據移到 GPU
    tensor = torch.tensor(data, device='mps')
    # 模擬一些 GPU 計算
    await asyncio.sleep(2)  # 模擬計算時間
    result = torch.sum(tensor).item()
    return result

N = 10**8
# 模擬 CPU 任務 - 異步
async def acal(a, b):
    start = time.time()
    for x in range(N):
        a += x
        a -= x
    process = time.time() - start
    return {"value": a+b, "process_time": process}

# 模擬 CPU 任務 - 同步
def cal(a, b):
    start = time.time()
    for x in range(N):
        a += x
        a -= x
    process = time.time() - start
    return {"value": a+b, "process_time": process}

#########################################################

class GPUInput(BaseModel):
    data    : List[float]

class CPUInput(BaseModel):
    a       : int
    b       : int


app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse("<html><head><title>大語言模型開發</title></head><body><h1>這裡是大語言模型開發測試環境</h1></body></html>")


@app.post("/gpu/1")
async def gpu(input: GPUInput):
    print("connect!")
    response = await gpu_task(data=input.data)
    print("success!")
    return response

@app.post("/cpu/acal/1")
async def cpu_acal(input: CPUInput):
    print("connect!")
    response = await acal(input.a, input.b)
    print("success!")
    return response

@app.post("/cpu/cal/0")
async def cpu_cal0(input: CPUInput):
    print("connect!")
    response = cal(input.a, input.b)
    print("success!")
    return response

@app.post("/cpu/cal/1")
def cpu_cal1(input: CPUInput):
    print("connect!")
    response = cal(input.a, input.b)
    print("success!")
    return response

@app.post("/cpu/cal/2")
async def cpu_cal2(input: CPUInput):
    print("connect!")
    response = await loop.run_in_executor(executor, partial(cal, input.a, input.b))
    print("success!")
    return response



@app.middleware("http")
async def middleware_control(request: Request, call_next):
    global client_tasks
    ## Before Response
    request.state.start_time = time.time()
    client_ip = request.client.host
    if client_tasks[client_ip] > 5:
        raise HTTPException(status_code=429, detail="Too many requests. Please wait for your previous task to completes.")
    client_tasks[client_ip] += 1
    ## Await for Response
    try:
        response = await call_next(request)
        ## After Response
        response.headers["X-Process-Time"] = str( time.time() - request.state.start_time )
        return response
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        client_tasks[client_ip] -= 1


@app.on_event("startup")
async def startup_event():
    global executor, loop, client_tasks
    loop = asyncio.get_event_loop()                 # 取得事件序列
    executor = ThreadPoolExecutor(max_workers=1)    # 執行器設定(目前設定1指一個GPU)
    client_tasks = defaultdict(int)                 # 追蹤客戶端請求發送現況

@app.on_event("shutdown")
async def shutdown_event():
    global executor
    if executor:
        executor.shutdown()                         # 關閉執行器