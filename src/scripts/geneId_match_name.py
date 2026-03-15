import pandas as pd
from pathlib import Path

base = Path(__file__).resolve().parent.parent

# 读取文件
expr = pd.read_csv(base / "data/expression/gene_expression_long.csv")
gene_info = pd.read_csv(base / "data/transcriptome/gene_infos.tsv", sep="\t", usecols=[0,1])
gene_info.columns = ["geneId", "geneName"]

# 检查是否有重复
dup = gene_info[gene_info.duplicated("geneId", keep=False)]
print(dup)

# merge
merged = expr.merge(gene_info, on="geneId", how="left")

# 检查是否有缺失geneName
missing = merged[merged["geneName"].isna()]["geneId"].unique()

print("未匹配到geneName的geneId数量:", len(missing))

if len(missing) > 0:
    print("示例缺失geneId:", missing[:10])

# 保存新文件
merged.to_csv(base / "data/expression/gene_expression_with_name.csv", index=False)

print("补全完成！")