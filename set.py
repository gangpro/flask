text = 'hello'
text_set = set(text)
print(text_set)  # {'o', 'H', 'l', 'e'}  # 중복을 허용하지 않음.


text2 = 'hi'
text_set2 = set(text2)
print(text_set2)


print(text_set & text_set2)  # 교집합 찾기
print(text_set | text_set2)  # 합집합 찾기

