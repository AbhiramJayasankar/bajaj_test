from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

class DataRequest(BaseModel):
    data: List[str]

class DataResponse(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str

def process_data(data: List[str]):
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    numbers_sum = 0
    
    for item in data:
        if item.isdigit():
            num = int(item)
            if num % 2 == 0:
                even_numbers.append(item)
            else:
                odd_numbers.append(item)
            numbers_sum += num
        elif item.isalpha():
            alphabets.append(item.upper())
        elif not item.isalnum():
            special_characters.append(item)
    
    return odd_numbers, even_numbers, alphabets, special_characters, str(numbers_sum)

def create_concat_string(alphabets: List[str]):
    all_chars = ''.join(alphabets)
    reversed_chars = all_chars[::-1]
    
    result = ""
    for i, char in enumerate(reversed_chars):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    
    return result

@app.post("/bfhl")
async def process_bfhl(request: DataRequest):
    try:
        odd_numbers, even_numbers, alphabets, special_characters, sum_str = process_data(request.data)
        concat_string = create_concat_string(alphabets)
        
        response = DataResponse(
            is_success=True,
            user_id="john_doe_17091999",
            email="john@xyz.com",
            roll_number="ABCD123",
            odd_numbers=odd_numbers,
            even_numbers=even_numbers,
            alphabets=alphabets,
            special_characters=special_characters,
            sum=sum_str,
            concat_string=concat_string
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")

@app.get("/")
async def root():
    return {"message": "BFHL API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)