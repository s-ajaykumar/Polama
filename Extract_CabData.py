import json

files = json.load(open('datasets/dstc8-schema-guided-dialogue/test/dialogues_033.json'))

#print(file)
count = 0
for i in files:
    turns = i['turns']
    for turn in turns:
        frames = turn['frames']
        for frame in frames:
            if frame['service'] == "RideSharing_2":
                count += 1
                print(f"{turn['speaker']}: {turn['utterance']}")
                with open('/Users/outbell/Ajay/DeepLearning/GenAI/Australia_Project/datasets/dstc8-schema-guided-dialogue/cab_data.txt', 'a') as w:
                    w.write(f"{turn['speaker']}: {turn['utterance']}\n")
                if count %2 == 0:
                    print("\n\n")
                    with open('/Users/outbell/Ajay/DeepLearning/GenAI/Australia_Project/datasets/dstc8-schema-guided-dialogue/cab_data.txt', 'a') as w:
                        w.write("\n\n")
        