import json

files = [
    "../data/transcriptome/gene_info.json",
    "../data/transcriptome/transcript_info.json"
]

for file in files:
    with open(file, "r") as f:
        data = json.load(f)

    # 只保留前100条
    small_data = data[:100]

    with open(file, "w") as f:
        json.dump(small_data, f, indent=2)

    print(f"{file} ✅ 已瘦身到 {len(small_data)} 条")