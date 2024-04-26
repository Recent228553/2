import os
import json
from get_block.get_block_by_index_linear import get_block_by_index_linear as get_block_linear
from get_block.get_block_by_idnex_binary import get_block_by_index_binary as get_block_binary
from sort.bubble_sort import bubble_sort as bubble_sort
from sort.selection_sort import selection_sort
from datetime import datetime, date


transactions_files = []
transactions_list = []
transactions_files += os.listdir('transactions')
for file_name in transactions_files:
    file = open(f"{'transactions'}/{file_name}")
    transactions_list.append(json.loads(file.read()))
a_copy = transactions_list.copy()

first_block = a_copy[0]
last_block = a_copy[-1]
mid_block = a_copy[len(a_copy)//2]
previous_20th_block = a_copy[len(a_copy)-20]
blocks_to_search = [first_block, last_block, mid_block, previous_20th_block]


# Task 1
linear_search_enabled = True
if linear_search_enabled:
    print("Linear Search:")
    for block in blocks_to_search:
        print(f"Linear Search for index {block['index']}: ", get_block_linear(a_copy, block['index']), sep="\n", end="\n")

    print("Sorted Linear Search:")
    for block in blocks_to_search:
        print(f"Linear Search for index {block['index']}: ", get_block_linear(sorted(a_copy, key=lambda x: x['index']), block['index']), sep="\n", end="\n")

    print("Binary Search:")
    for block in blocks_to_search:
        print(f"Binary Search for index {block['index']}: ", get_block_binary(a_copy, block['index']), sep="\n", end="\n")


# Task 2
sorting_enabled = True
if sorting_enabled:
    print(f"Unsorted Array: \n")
    print(f"Bubble Sort:\n {bubble_sort(a_copy)}")
    print(f"Selection Sort:\n {selection_sort(a_copy)}")


# Task 3
transactions_analysis_enabled = True
if transactions_analysis_enabled:
    total_transactions_count = 0
    count_without_system = 0
    sorted_blocks = sorted(a_copy, key=lambda x: x['index'])
    miners_dict = dict()

    for block in sorted_blocks:
        total_transactions_count += len(block['transactions'])
        count_without_system += len(list(filter(lambda x: x['from'] != "SYSTEM" and block['index'] != 0, block['transactions'])))
        print(f"Block Number: {block['index']}. Number of Transactions: {len(block['transactions'])}")

    print(f"Total Number of Transactions: {total_transactions_count}; {count_without_system} (excluding SYSTEM)\n")

    list_of_rewards = []
    list_of_transactions_values = []

    for block in sorted_blocks:
        if block["index"] == 0:
            continue
        list_of_rewards.append(block["transactions"][-1]["value"])
        if block['transactions'][-1]['to'] not in miners_dict:
            miners_dict[block['transactions'][-1]['to']] = 0
        miners_dict[block['transactions'][-1]['to']] += block['transactions'][-1]['value']
    miners_dict = sorted(miners_dict.items(), key=lambda x: x[1])
    list_of_rewards = sorted(list_of_rewards)

    print(f"Lowest Reward: {miners_dict[0]}\nHighest Reward: {miners_dict[-1]}\n")
    print(f"Lowest Reward Value: {list_of_rewards[0]}\nHighest Reward Value: {list_of_rewards[-1]}\n")


    for block in sorted_blocks:
        if block["index"] == 0:
            continue
        for transaction in block["transactions"]:
            if transaction['from'] == "SYSTEM":
                continue
            list_of_transactions_values.append(transaction["value"])
    print(f"Average Transaction Value: {sum(list_of_transactions_values)/len(list_of_transactions_values)}")
    minutes_dict = {}


    for block in sorted_blocks:
        minute = datetime.fromtimestamp(block['timestamp']).minute
        if minute not in minutes_dict:
            minutes_dict[minute] = 0
        else:
            minutes_dict[minute] += 1

    print("\n Minutes:")
    for key, val in minutes_dict.items():
        print(f"{key} min: {val}")