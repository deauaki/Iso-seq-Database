<template>
  <section class="population-expression">
    <el-input v-model="keyword" aria-label="Gene ID or name" placeholder="Gene ID or name" @keyup.enter.native="search" />
    <el-button type="primary" @click="search">Query gene</el-button>
    <p v-if="!gene">Try DEMO-GENE-1 or DEMO-GENE-2.</p>
    <template v-else>
      <p>{{ gene.geneId }} · {{ gene.cohortId }} · {{ gene.tissue }} <el-tag size="small" type="info">Demo data</el-tag></p>
      <el-checkbox-group v-model="populations" @change="updateCharts">
        <el-checkbox v-for="group in gene.groups" :key="group.populationId" :label="group.populationId">
          {{ group.populationId }} (n={{ group.samples.length }})
        </el-checkbox>
      </el-checkbox-group>
      <p v-if="!populations.length">Select a population to show expression.</p>
      <div class="population-charts">
        <div v-for="chart in charts" :key="chart.ref" class="population-chart">
          <div :ref="chart.ref" :style="{ minWidth: chartMinWidth(chart.ref) + 'px' }" />
        </div>
      </div>
      <p>Usage is calculated per sample from the sum of displayed transcript TPMs. Samples with a zero sum are excluded from usage.</p>
    </template>
  </section>
</template>

<script>
import Plotly from 'plotly.js-dist'
import { getDemoGeneExpression } from '@/api/demoTranscriptome'

const charts = [
  { ref: 'geneTpm', title: 'Gene total', unit: 'TPM' },
  { ref: 'transcriptTpm', title: 'Transcript expression', unit: 'TPM' },
  { ref: 'usage', title: 'Transcript usage', unit: '%' }
]

export default {
  data() {
    return { charts, keyword: 'DEMO-GENE-1', gene: null, populations: [] }
  },
  watch: {
    '$route.query.keyword': {
      immediate: true,
      handler(keyword) {
        if (typeof keyword === 'string') this.keyword = keyword
        this.search()
      }
    }
  },
  mounted() {
    if (typeof ResizeObserver !== 'undefined') {
      this.chartObserver = new ResizeObserver(() => {
        if (!this.populations.length) return
        charts.forEach(({ ref }) => {
          const chart = this.chartElement(ref)
          if (chart && chart._fullLayout) Plotly.Plots.resize(chart)
        })
      })
      this.chartObserver.observe(this.$el)
    }
  },
  beforeDestroy() {
    if (this.chartObserver) this.chartObserver.disconnect()
    this.purgeCharts()
  },
  methods: {
    async search() {
      const gene = await getDemoGeneExpression(this.keyword)
      this.purgeCharts()
      this.gene = gene
      this.populations = gene ? gene.groups.map(group => group.populationId) : []
      this.updateCharts()
    },
    updateCharts() {
      this.$nextTick(this.renderCharts)
    },
    chartElement(ref) {
      return this.$refs[ref] && this.$refs[ref][0]
    },
    chartMinWidth(ref) {
      const categoryCount = ref === 'geneTpm' ? 1 : this.gene.transcripts.length
      return 80 + 48 * this.populations.length * categoryCount
    },
    purgeCharts() {
      charts.forEach(({ ref }) => {
        const chart = this.chartElement(ref)
        if (chart) Plotly.purge(chart)
      })
    },
    renderCharts() {
      if (!this.gene) return
      if (!this.populations.length) {
        this.purgeCharts()
        return
      }

      charts.forEach(({ ref, title, unit }) => {
        const traces = this.gene.groups.filter(group => this.populations.includes(group.populationId)).map(group => {
          const ids = ref === 'geneTpm' ? [this.gene.geneId] : this.gene.transcripts.map(tx => tx.transcriptId)
          const samples = ref === 'usage'
            ? group.samples.filter(sample => Object.values(sample.transcriptTpm).some(tpm => tpm > 0))
            : group.samples
          const x = []
          const y = []
          ids.forEach(id => {
            samples.forEach(sample => {
              x.push(id)
              if (ref === 'geneTpm') {
                y.push(sample.geneTpm)
              } else if (ref === 'usage') {
                const total = Object.values(sample.transcriptTpm).reduce((sum, tpm) => sum + tpm, 0)
                y.push(100 * sample.transcriptTpm[id] / total)
              } else {
                y.push(sample.transcriptTpm[id])
              }
            })
          })
          return {
            type: 'violin',
            name: group.populationId + ' (n=' + samples.length + ')',
            x,
            y,
            spanmode: 'hard',
            points: 'all',
            meanline: { visible: true }
          }
        })

        Plotly.react(this.chartElement(ref), traces, {
          autosize: true,
          height: 380,
          title: { text: title },
          yaxis: { title: { text: unit }, rangemode: 'tozero' },
          violinmode: 'group',
          legend: { orientation: 'h' },
          xaxis: { automargin: true },
          margin: { l: 52, r: 15, t: 55, b: 65 }
        }, { responsive: true, displayModeBar: false })
      })
    }
  }
}
</script>

<style scoped>
.population-expression {
  padding: 20px;
  margin-bottom: 24px;
  background: #f6f6f6;
}
.el-input {
  width: 200px;
  margin-right: 8px;
}
.population-charts {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 16px;
  margin-top: 16px;
}
.population-chart {
  width: 100%;
  min-width: 0;
  overflow-x: auto;
}
</style>
