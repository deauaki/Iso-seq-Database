<template>
  <div ref="chart" aria-label="Mean phenotype by genotype" />
</template>

<script>
import Plotly from 'plotly.js-dist'

export default {
  props: {
    groups: { type: Array, required: true }
  },
  mounted() {
    Plotly.newPlot(this.$refs.chart, [{
      type: 'bar',
      x: this.groups.map(group => group.genotype + ' (n=' + group.n + ')'),
      y: this.groups.map(group => group.mean)
    }], {
      title: { text: 'Mean standardized phenotype by genotype' },
      yaxis: { title: { text: 'Mean (demo units)' }},
      height: 300,
      margin: { t: 55, b: 45 }
    }, { responsive: true, displayModeBar: false })
  },
  beforeDestroy() {
    Plotly.purge(this.$refs.chart)
  }
}
</script>
