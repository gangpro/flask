userinput = '1 2 3 4 5 6'
print(userinput.split())  # 결과값 String   # ['1', '2', '3', '4', '5', '6']

list_expression = [f'숫자{i}' for i in range(6)]
print(list_expression)  # 결과값 String   # ['숫자0', '숫자1', '숫자2', '숫자3', '숫자4', '숫자5']

list_expression = [int(num) for num in userinput.split()]
print(list_expression)  # 결과값 Int   # [1, 2, 3, 4, 5, 6]




