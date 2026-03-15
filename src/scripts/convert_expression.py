import pandas as pd
from pathlib import Path

base = Path(__file__).resolve().parent.parent

gene_file = base / "data/expression/gene_expression_with_name.csv"
tx_file = base / "data/expression/transcript_expression_long.csv"

out_dir = base / "data/expression"

gene_df = pd.read_csv(gene_file)
gene_df.to_json(out_dir / "gene_expression.json", orient="records", indent=2)

tx_df = pd.read_csv(tx_file)
tx_df.to_json(out_dir/ "transcript_expression.json", orient="records", indent=2)

print("✅ .json generated")