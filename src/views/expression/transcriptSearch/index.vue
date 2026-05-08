<template>
  <div class="page-container">

    <!-- 查询区域 -->
    <div class="search-panel">

      <el-input
        v-model="keyword"
        placeholder="transcript ID"
        clearable
        class="search-input"
        @keyup.enter.native="searchTranscript"
      />

      <el-button
        type="primary"
        @click="searchTranscript"
      >
        Query Transcript Expression
      </el-button>

      <el-button
        type="info"
        @click="resetSearch"
      >
        Reset
      </el-button>

      <el-switch
        v-model="useLog"
        active-text="log2(expression+1)"
        @change="searchTranscript"
      />

    </div>

    <!-- 图表区域 -->

    <div
      ref="chart"
      v-loading="loading"
      class="chart-container"
    />

  </div>
</template>

<script>
import Plotly from 'plotly.js-dist'
import transcriptData from '@/data/expression/transcript_expression.json'

export default {

  name: 'TranscriptExpressionViolin',

  data() {

    return {

      keyword: '',

      rawData: [],

      loading: false,

      useLog: false

    }

  },

  mounted() {

    this.rawData = transcriptData

    window.addEventListener('resize', this.handleResize)

  },

  beforeDestroy() {

    window.removeEventListener('resize', this.handleResize)

  },

  methods: {

    handleResize() {

      Plotly.Plots.resize(this.$refs.chart)

    },

    searchTranscript() {

      const key = this.keyword.trim()

      if (!key) {

        this.$message.warning('请输入转录本ID')

        return

      }

      this.loading = true

      setTimeout(() => {

        const matched = this.rawData.filter(item =>

          item.transcriptId
            .trim()
            .toLowerCase() === key.toLowerCase()

        )

        if (!matched.length) {

          this.$message.warning('未找到该转录本')

          Plotly.purge(this.$refs.chart)

          this.loading = false

          return

        }

        const grouped = {}

        matched.forEach(item => {

          const id = item.transcriptId

          if (!grouped[id]) {

            grouped[id] = []

          }

          let val = Number(item.expression)

          if (this.useLog) {

            val = Math.log2(val + 1)

          }

          grouped[id].push(val)

        })

        const labels = Object.keys(grouped)

        const data = labels.map(g => grouped[g])

        this.drawChart(labels, data)

        this.loading = false

      }, 150)

    },

    resetSearch() {

      this.keyword = ''

      this.useLog = false

      Plotly.purge(this.$refs.chart)

    },

    drawChart(labels, data) {

      const traces = labels.map((label, i) => ({

        type: 'violin',

        orientation: 'h',

        x: data[i],

        y: Array(data[i].length).fill(label),

        name: label,

        box: {
          visible: true
        },

        meanline: {
          visible: true
        },

        points: 'all',

        jitter: 0.25,

        pointpos: 0,

        marker: {
          size: 4,
          opacity: 0.5
        },

        line: {
          width: 1.2
        },

        hovertemplate:
          '<b>%{y}</b><br>' +
          'Expression: %{x}<extra></extra>'

      }))

      const layout = {

        title: {

          text: 'Transcript Expression Distribution',

          font: {
            size: 22
          }

        },

        xaxis: {

          title: this.useLog
            ? 'log2(Expression + 1)'
            : 'Expression',

          zeroline: false

        },

        yaxis: {

          automargin: true,

          title: {
            text: 'Transcript ID'
          }

        },

        height: 520,

        margin: {
          l: 120,
          r: 40,
          t: 60,
          b: 60
        },

        plot_bgcolor: '#ffffff',

        paper_bgcolor: '#ffffff',

        showlegend: false

      }

      const config = {

        responsive: true,

        displayModeBar: true

      }

      Plotly.newPlot(
        this.$refs.chart,
        traces,
        layout,
        config
      )

    }

  }

}
</script>

<style scoped>

.page-container {
  padding: 25px;
}

.search-panel {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-input {
  width: 260px;
}

.search-panel .el-button {
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
}

.search-panel .el-button.el-button--primary {
  background-color: #4e73df;
  border-color: #4e73df;
}

.search-panel .el-button.el-button--primary:hover {
  background-color: #3558c2;
  border-color: #3558c2;
}

.search-panel .el-button.el-button--info {
  background-color: #a0aec0;
  border-color: #a0aec0;
}

.search-panel .el-button.el-button--info:hover {
  background-color: #7b8794;
  border-color: #7b8794;
}

.chart-container {
  width: 100%;
  height: 600px;
  background: white;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

</style>