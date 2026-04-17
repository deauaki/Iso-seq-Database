<template>
  <div class="page-container">

    <!-- 查询区域 -->
    <div class="search-panel">

      <el-input
        v-model="keyword"
        placeholder="transcript Id "
        clearable
        class="search-input"
        @keyup.enter.native="searchTranscript"
      />

      <el-button type="primary" @click="searchTranscript">Query Transcript Expression</el-button>
      <el-button type="info" @click="resetSearch">Reset</el-button>

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
import * as echarts from 'echarts'
import transcriptData from '@/data/expression/transcript_expression.json'

export default {

  name: 'TranscriptExpressionViolin',

  data() {
    return {

      keyword: '',

      rawData: [],

      chart: null,

      loading: false,

      useLog: false

    }
  },

  mounted() {
    this.rawData = transcriptData

    this.chart = echarts.init(this.$refs.chart)

    window.addEventListener('resize', () => {
      this.chart.resize()
    })
  },

  methods: {
    searchTranscript() {
      const key = this.keyword.trim()

      if (!key) {
        this.$message.warning('请输入转录本ID')
        return
      }

      this.loading = true

      setTimeout(() => {
        const matched = this.rawData.filter(item =>
          item.transcriptId.trim().toLowerCase() === key.toLowerCase()
        )

        if (!matched.length) {
          this.$message.warning('未找到该转录本')

          this.chart.clear()

          this.loading = false

          return
        }

        const grouped = {}

        matched.forEach(item => {
          const id = item.transcriptId

          if (!grouped[id]) grouped[id] = []

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

      this.chart.clear()
    },

    drawChart(labels, data) {
      const scatterData = []

      data.forEach((arr, i) => {
        arr.forEach(v => {
          scatterData.push([v, i])
        })
      })

      const option = {

        tooltip: {
          trigger: 'item'
        },

        grid: {
          left: 120,
          right: 50,
          bottom: 50,
          top: 40
        },

        xAxis: {
          type: 'value',
          name: this.useLog ? 'log2(Expression+1)' : 'Expression',
          nameLocation: 'middle',
          nameGap: 30
        },

        yAxis: {
          type: 'category',
          data: labels,
          name: 'TranscriptId'
        },

        series: [

          {
            name: 'boxplot',
            type: 'boxplot',
            data: data
          },

          {
            name: 'points',
            type: 'scatter',
            data: scatterData,
            symbolSize: 6,
            itemStyle: {
              opacity: 0.6
            }
          }

        ]

      }

      this.chart.setOption(option)
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

.search-input {
  width: 260px;
}

.chart-container {
  width: 100%;
  height: 520px;
  background: white;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

</style>
