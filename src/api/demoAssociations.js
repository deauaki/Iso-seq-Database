import associations from '@/data/mock/qtlAssociations.json'
import variants from '@/data/mock/variants.json'

function matchesKeyword(fields, keyword) {
  return fields.some(field => field && field.toUpperCase().includes(keyword))
}

export async function getQtlAssociations({ type, keyword }) {
  const key = keyword.trim().toUpperCase()
  return associations.filter(row => row.type === type &&
    matchesKeyword([row.geneId, row.transcriptId, row.variantId], key))
}

export async function getVariants(keyword) {
  const key = keyword.trim().toUpperCase()
  return variants.filter(row => matchesKeyword([row.variantId, row.chrom + ':' + row.pos], key))
}

export async function getVariant(id) {
  return variants.find(row => row.variantId === id)
}
