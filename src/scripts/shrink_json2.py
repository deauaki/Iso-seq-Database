import json

# 要处理的文件
files = [
    '../data/expression/gene_expression.json',
    '../data/expression/transcript_expression.json'
]

# 保留前10个 sample
KEEP_SAMPLE_NUM = 10

for file in files:

    print(f'\n正在处理: {file}')

    with open(file, 'r') as f:
        data = json.load(f)

    # 提取前10个 sampleId
    sample_ids = []

    for item in data:

        sid = item['sampleId']

        if sid not in sample_ids:

            sample_ids.append(sid)

        if len(sample_ids) >= KEEP_SAMPLE_NUM:

            break

    # 只保留这些 sample 的数据
    small_data = [

        item for item in data
        if item['sampleId'] in sample_ids

    ]

    # 覆盖写回
    with open(file, 'w') as f:

        json.dump(small_data, f, indent=2)

    print(f'保留 sample:')
    print(sample_ids)

    print(f'剩余数据: {len(small_data)} 条')