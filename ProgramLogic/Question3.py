# Joe.Shih的國泰世華數位銀行部的考題測驗
# 1-3 一到三報數
import random


def count_number(input_number):
    limit = 3
    ans = input_number % limit
    if input_number == 0 or input_number < limit:
        return input_number  # 輸入0，或是小於3
    elif ans == 0:
        return limit  # 可被整除就是3
    else:
        return ans  # 餘數


total_number = random.randrange(100)  # 產生0~100的亂數
which_seat = count_number(total_number)
print('總人數：' + str(total_number))
print('順位：' + str(which_seat))
