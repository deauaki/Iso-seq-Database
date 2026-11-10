import genes from '@/data/mock/transcriptExpression.json'

export function getDemoTranscripts() {
  return [].concat(...genes.map(({ geneId, geneName, transcripts }) =>
    transcripts.map(transcript => ({ ...transcript, geneId, geneName, isDemo: true })))
  )
}

export function getDemoGeneExpression(keyword) {
  const key = keyword.trim().toUpperCase()
  return Promise.resolve(genes.find(gene => gene.geneId === key || gene.geneName === key))
}
