# Joe.Shih的國泰世華數位銀行部的考題測驗
# 1-3 一到三報數
import random


def find_last_person(n):
    if n == 0:
        return '沒有人'

    people = list(range(1, n + 1))  # 建立人員列表，編號從1到n
    index = 0  # 目前報數的人的索引
    while len(people) > 1:
        index = (index + 2) % len(people)  # 跳過3個人，取餘數避免索引超出範圍
        del people[index]  # 退出圈子
    return people[0]  # 返回最後留下的人的編號


QA_peoples =  random.randrange(100)  # 產生0~100的亂數至QA人數
last_person = find_last_person(QA_peoples)
print("QA總人數：", QA_peoples)
print("最後留下的人的順位：", last_person)
