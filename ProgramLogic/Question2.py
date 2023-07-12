# Joe.Shih的國泰世華數位銀行部的考題測驗
# 1-2 計算字卡

def count_characters(input_text):
    input_text = input_text.replace(' ', '')  # 將字串去除空格
    input_text = input_text.upper()  # 將字串都轉換為大寫
    input_text = ''.join(sorted(input_text))  # 排序
    char_map = {}
    return_str = ''
    for char in input_text:
        if char in char_map:
            char_map[char] += 1
        else:
            char_map[char] = 1
    for char, count in char_map.items():
        return_str += f'{char} {count}\n'  # 格式化並換行再加總至return
    return return_str


string = 'Hello welcome to Cathay 60th year anniversary'
chat_cards = count_characters(string)
print(chat_cards)
