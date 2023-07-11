# Joe.Shih的國泰世華數位銀行部的考題測驗
# 1-1 數字顛倒輸出

def reverse_numbers(numbers):
    return_list = []
    for num in numbers:
        num_str = str(num)
        converted_str = num_str[::-1]  # 陣列反向讀取
        converted_num = int(converted_str)
        return_list.append(converted_num)
    return return_list


score = [35, 46, 57, 91, 29]
correct_score = reverse_numbers(score)
print(correct_score)  # 輸出: [53, 64, 75, 19, 92]
