import results from '@/data/mock/differentialResults.json'

export function getDifferentialContrasts() {
  return Object.values(results.reduce((contrasts, { analysisId, contrast }) => {
    contrasts[analysisId] = { analysisId, ...contrast }
    return contrasts
  }, {}))
}

export function getDifferentialResults({ type, analysisId, keyword, significantOnly, page, pageSize }) {
  const key = keyword.trim().toUpperCase()
  const matches = results.filter(row =>
    row.type === type && row.analysisId === analysisId &&
    (!key || row.geneId.includes(key) || (row.transcriptId || '').includes(key)) &&
    (!significantOnly || (row.adjustedPValue != null && row.adjustedPValue < 0.05))
  )
  const start = (page - 1) * pageSize
  return Promise.resolve({
    code: 20000,
    data: { total: matches.length, items: matches.slice(start, start + pageSize) }
  })
}
