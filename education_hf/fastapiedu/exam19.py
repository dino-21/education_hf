from typing import List, Optional, Union
from datetime import datetime

from pydantic import BaseModel, Field

class Movie(BaseModel):
	mid: int
	genre: str
	rate: Union[int, float] 
	tag: Optional[str] = None 
	date: Optional[datetime] = None 
	some_variable_list: List[int] = [] 

class User(BaseModel):
	'''
	gt : 설정된 값보다 큰 
	ge : 설정된 값보다 크거나 같은
	lt : 설정된 값보다 작은 
	le : 설정된 값보다 작거나 같은
	'''
	uid: int
	name: str = Field(min_length=2, max_length=7)
	age: int = Field(gt=20, le=30)

tmp_movie_data = {
	'mid' : '1',
	'genre' : 'action',
	'rate' : 1.5,
	'tag' : None,
	'date' : '2024-01-03T19:12:11'
}

tmp_user_data = {
	'uid' : '100',
	'name' : '가나다',
	'age' : 31
}

tmp_movie = Movie(**tmp_movie_data)
tmp_user_data = User(**tmp_user_data)
print(tmp_movie.model_dump_json())
print(tmp_user_data.model_dump_json())
print(tmp_user_data.name)

class DataInput(BaseModel):
	user_id: int = Field(ge=0, le=1000)
	movie_id:int = Field(ge=0, le=500)
	gender:int = Field(ge=0, le=1)
	age:int = Field(ge=0, le=6)
	genre:int = Field(ge=0, le=10)

tmp_movie_data = {
	'user_id' : 10,
	'movie_id' : 3,
	'gender' : 0,
	'age' : 6,
	'genre' : 10
}
tmp_movie_data = DataInput(**tmp_movie_data)
print(tmp_movie_data.model_dump_json())



